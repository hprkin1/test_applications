import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import csv

def send_bulk_emails(sender_email, sender_password, recipients, subject, body):
    """
    Send standardized email to multiple recipients.
    
    Args:
        sender_email (str): Sender's email address
        sender_password (str): Sender's email password or app password
        recipients (list): List of recipient email addresses
        subject (str): Email subject line
        body (str): Email body content
    """
    # Set up the SMTP server (using Gmail as example)
    # For other providers, change the SMTP server and port
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        
        # Login to the email account
        server.login(sender_email, sender_password)
        print(f"Logged in successfully as {sender_email}")
        
        # Send email to each recipient
        for recipient in recipients:
            # Create message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject
            
            # Add body to email
            message.attach(MIMEText(body, 'plain'))
            
            # Convert message to string and send
            text = message.as_string()
            server.sendmail(sender_email, recipient, text)
            print(f"Email sent successfully to {recipient}")
        
        # Close the server connection
        server.quit()
        print("\nAll emails sent successfully!")
        
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check your email and password.")
        print("For Gmail, you may need to use an App Password instead of your regular password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_recipients_from_csv(csv_file_path):
    """
    Read email addresses and names from CSV file.
    Returns a list of dictionaries with 'email' and 'name' keys.
    """
    recipients = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Strip whitespace from column names and values
                email = row.get('Email', '').strip()
                name = row.get('Name', '').strip()
                
                if email:  # Only add if email exists
                    recipients.append({
                        'email': email,
                        'name': name
                    })
        
        print(f"Successfully loaded {len(recipients)} recipients from CSV")
        return recipients
    
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


if __name__ == "__main__":
    # Configuration
    sender_email = input("Enter your email address: ")
    sender_password = getpass.getpass("Enter your password (or app password): ")
    
    # Read recipients from CSV file
    csv_file = "skeldale-house-prize-draw-2025-11-01 - Sheet1.csv"
    recipient_list = read_recipients_from_csv(csv_file)
    
    if not recipient_list:
        print("No recipients found. Exiting.")
        exit()
    
    # Extract just the email addresses for sending
    recipients = [r['email'] for r in recipient_list]
    
    # Email content
    subject = "Your Subject Here"
    body = """Hello,

This is a standardized email message being sent to multiple recipients.

You can customize this message as needed.

Best regards,
Your Name
"""
    
    # Optional: Personalize emails with names
    # If you want to personalize each email, you can modify the send function
    # For now, sending the same message to all
    
    # Send emails
    send_bulk_emails(sender_email, sender_password, recipients, subject, body)


# SMTP Server Settings for Common Email Providers:
# Gmail: smtp.gmail.com, port 587
# Outlook/Hotmail: smtp-mail.outlook.com, port 587
# Yahoo: smtp.mail.yahoo.com, port 587
# Office 365: smtp.office365.com, port 587
