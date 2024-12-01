import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Lista osób i ich współmałżonków z adresami e-mail
participants = {
    "V": {"spouse": "J", "email": "v@gmail.com"},
    "J": {"spouse": "V", "email": "j@gmail.com"},
    "D": {"spouse": "", "email": "d@gmail.com"},
    "M": {"spouse": "D", "email": "k@gmail.com"},
    "K": {"spouse": "T", "email": "k@gmail.com"},
    "T": {"spouse": "K", "email": "t@gmail.com"}
}

# Funkcja losująca, która zapewnia spełnienie warunków
def draw_gifts(participants):
    givers = list(participants.keys())
    receivers = givers[:]
    random.shuffle(receivers)

    # Powtarzamy losowanie, dopóki są konflikty
    while any(giver == receiver or participants[giver]["spouse"] == receiver for giver, receiver in zip(givers, receivers)):
        random.shuffle(receivers)

    # Tworzymy pary
    return {giver: receiver for giver, receiver in zip(givers, receivers)}

# Funkcja do wysyłania e-maili
def send_email(sender_email, sender_password, recipient_email, giver, receiver):
    subject = "Twój wylosowany na święta 🎁 - to losowanie zastępuje poprzednie"
    body = f"Cześć {giver},\n\nTwoim zadaniem jest kupienie prezentu dla: {receiver}.\n\nWesołych Świąt!"

    # Tworzymy wiadomość e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Konfiguracja SMTP (tu przykład dla Gmaila)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"E-mail wysłany do {giver} ({recipient_email})")
    except Exception as e:
        print(f"Błąd przy wysyłaniu e-maila do {giver}: {e}")

# Główna logika programu
def main():
    sender_email = "t@gmail.com"  # Wpisz swój adres e-mail
    sender_password = "**** **** **** ****"  # Wpisz hasło aplikacji bez spacji

    result = draw_gifts(participants)
    print("Losowanie zakończone. Wysyłanie e-maili...")

    for giver, receiver in result.items():
        recipient_email = participants[giver]["email"]
        send_email(sender_email, sender_password, recipient_email, giver, receiver)

    print("Wszystkie wiadomości zostały wysłane.")

# Uruchomienie programu
if __name__ == "__main__":
    main()
