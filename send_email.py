def send_email(text):
    import yagmail
    emails_list =
    print('start send emails ...')
        


    #config email smtp
    yag = yagmail.SMTP(

    #send email
    yag.send(emails_list,
            'server update',
            text)

    return None
