import script
import threading

from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Fetch form data

        userDetails = request.form
        
        email = userDetails['mail']
        
        num = userDetails['Submit']
        num=num.split(' ')
        num=int(num[1],10)

        arg = email + "  "

        for i in range(1,num+1):

            arg += userDetails[str(i)+"url"]+"  "

            arg += str(userDetails[str(i)+"price"])+"  "


        threading.Thread(target=script.main, args=(arg,)).start()     

        return render_template('sucess.html',email=email)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)