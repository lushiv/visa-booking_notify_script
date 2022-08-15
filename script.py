try:
    from urllib import response
    import  requests
    import  json
    import time
    import sendgrid
    import  os
    import schedule
    import  bs4
    from sendgrid.helpers.mail import *

except Exception as e:
    print("some modules are not installed: %s"%e)

SLEEP_TIME = 10 # seconds
MAIN_URL = "https://konepembappointment.com/visa/booking"

CONF_JSON = {
    "api_key": "",
    "from_email": "",
    "to_email": "121ajaya@gmail.com",
    "subject": "Notify For Visa is available"
}


def SendEmailHelperFun(body):
    sendgrid_connection = None
    try:
        print("sending email........................................................")
        sendgrid_connection = sendgrid.SendGridAPIClient(api_key=CONF_JSON.get('api_key'))

        message = Mail(
        from_email=CONF_JSON.get('from_email'),
        to_emails= CONF_JSON.get('to_email'),
        subject=CONF_JSON.get('subject'),
        html_content=body)

        print("trying sending email on requesting payload is : %s"% message)
        response = sendgrid_connection.send(message)

        if response.status_code == 200:
            print("message sent successfully")
            return True

    except Exception as e:
        print(e)
        return False

    finally:
        print("send message successfully")



def VisbookingScript(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            response_body = response.text
            soup = bs4.BeautifulSoup(response_body, 'lxml')
            table1 = soup.find('table', id='booking_time_slots')

            for i in table1.find_all('label'):
                class_data = i.attrs.get('class')
                time = i.contents[0].split(" ")[4].split("\n")[0]
                print("Crawling data::::.....time is::%s......... %s"%(time, class_data[5]))

                if len(class_data) ==6 or class_data[5] =='disabled':
                    print("valid data is found.......time is %s"%time)
                    send_mail = SendEmailHelperFun("Visa available date is.......%s"%time)
                    if send_mail:
                        print('operation successful')
        else:
            print("************* Visbooking Still Script is running*************")
    except Exception as e:
        print(e)
    
    finally:
        print("script running completed")
    


VisbookingScript(MAIN_URL)

while True:
    print ("*"*60)
    print ('Script is running after .......%s seconds'%SLEEP_TIME)
    schedule.run_pending()
    time.sleep(SLEEP_TIME)
    VisbookingScript(MAIN_URL)
