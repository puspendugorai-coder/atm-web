from flask import Flask, render_template, request, redirect, url_for, session, flash
from supabase import create_client, Client
import os, time

app = Flask(__name__)
app.secret_key = "atm_secret_key_change_this"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://bryhzndcduqvfnjhgeub.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyeWh6bmRjZHVxdmZuamhnZXViIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTI4NjY2NSwiZXhwIjoyMDkwODYyNjY1fQ.Vg2c_mQTAQzBH9dsMdOh8WtetBuGKtQY4dnDolipma0")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

LOCK_DURATION = 60  # seconds


# ── HELPERS ────────────────────────────────────────────────────
def get_remaining_lock():
    unlock_time = session.get("atm_unlock_time", 0)
    remaining = int(unlock_time - time.time())
    return remaining if remaining > 0 else 0

def set_lockout():
    session["atm_unlock_time"] = time.time() + LOCK_DURATION

def is_locked():
    return get_remaining_lock() > 0


# ── STEP 1: CARD ENTRY ─────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def card_entry():
    # Clear previous ATM session on fresh visit
    if request.method == "GET":
        for key in ["card_no", "user_name", "current_balance", "pin_attempts", "mode"]:
            session.pop(key, None)

    if is_locked():
        return redirect(url_for("locked"))

    if request.method == "POST":
        card = request.form.get("card_no", "").strip()
        if not card:
            flash("Please enter your card number.", "error")
            return redirect(url_for("card_entry"))

        try:
            res = supabase.table("registration").select("Name").eq("Card_No", card).execute()
            if res.data:
                session["card_no"]   = card
                session["user_name"] = res.data[0]["Name"]
                session["pin_attempts"] = 0
                return redirect(url_for("menu"))
            else:
                flash("Invalid card number. Please try again.", "error")
        except Exception as e:
            flash(f"Connection error: {e}", "error")

    return render_template("atm.html", step="card")


# ── STEP 2: MENU ───────────────────────────────────────────────
@app.route("/menu")
def menu():
    if is_locked():
        return redirect(url_for("locked"))
    if "card_no" not in session:
        return redirect(url_for("card_entry"))
    return render_template("atm.html", step="menu", user_name=session.get("user_name"))


# ── STEP 3: PIN ENTRY ──────────────────────────────────────────
@app.route("/pin/<mode>", methods=["GET", "POST"])
def pin_entry(mode):
    if is_locked():
        return redirect(url_for("locked"))
    if "card_no" not in session:
        return redirect(url_for("card_entry"))

    if mode not in ["WITHDRAW", "DEPOSIT", "BALANCE"]:
        return redirect(url_for("menu"))

    if request.method == "POST":
        pin = request.form.get("pin", "").strip()
        card = session.get("card_no")

        try:
            res = supabase.table("registration").select("Pin_No, Amount").eq("Card_No", card).execute()
            if res.data and str(res.data[0]["Pin_No"]) == str(pin):
                session["pin_attempts"]    = 0
                session["current_balance"] = int(res.data[0]["Amount"])
                session["mode"]            = mode

                if mode == "BALANCE":
                    return redirect(url_for("show_balance"))
                else:
                    return redirect(url_for("amount_entry"))
            else:
                attempts = session.get("pin_attempts", 0) + 1
                session["pin_attempts"] = attempts
                remaining = 3 - attempts
                if attempts >= 3:
                    set_lockout()
                    return redirect(url_for("locked"))
                flash(f"Wrong PIN! {remaining} attempt(s) left.", "error")
        except Exception as e:
            flash(f"System error: {e}", "error")

    return render_template("atm.html", step="pin", mode=mode)


# ── STEP 4A: BALANCE ───────────────────────────────────────────
@app.route("/balance")
def show_balance():
    if "card_no" not in session:
        return redirect(url_for("card_entry"))
    balance = session.get("current_balance", 0)
    return render_template("atm.html", step="balance", balance=balance)


# ── STEP 4B: AMOUNT ENTRY ──────────────────────────────────────
@app.route("/amount", methods=["GET", "POST"])
def amount_entry():
    if is_locked():
        return redirect(url_for("locked"))
    if "card_no" not in session:
        return redirect(url_for("card_entry"))

    mode    = session.get("mode", "WITHDRAW")
    balance = session.get("current_balance", 0)

    if request.method == "POST":
        try:
            amt = int(request.form.get("amount", 0))
            if amt <= 0:
                flash("Amount must be greater than zero.", "error")
                return redirect(url_for("amount_entry"))

            if mode == "WITHDRAW":
                if amt > balance:
                    flash("Insufficient funds!", "error")
                    return redirect(url_for("amount_entry"))
                new_bal = balance - amt
            else:
                new_bal = balance + amt

            card = session.get("card_no")
            supabase.table("registration").update({"Amount": new_bal}).eq("Card_No", card).execute()
            session["current_balance"] = new_bal

            return render_template("atm.html", step="result",
                                   mode=mode, amount=amt, new_balance=new_bal)
        except ValueError:
            flash("Please enter a valid numeric amount.", "error")
        except Exception as e:
            flash(f"Transaction failed: {e}", "error")

    return render_template("atm.html", step="amount", mode=mode, balance=balance)


# ── LOCKED ─────────────────────────────────────────────────────
@app.route("/locked")
def locked():
    remaining = get_remaining_lock()
    if remaining <= 0:
        return redirect(url_for("card_entry"))
    return render_template("atm.html", step="locked", remaining=remaining)


# ── LOGOUT / RESET ─────────────────────────────────────────────
@app.route("/reset")
def reset():
    for key in ["card_no", "user_name", "current_balance", "pin_attempts", "mode"]:
        session.pop(key, None)
    return redirect(url_for("card_entry"))


if __name__ == "__main__":
    app.run(debug=True)