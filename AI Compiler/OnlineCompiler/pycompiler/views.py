import sys
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def runcode(request):

    if request.method == "POST":
        codeareadata = request.POST['codearea']

        try:
            original_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')

            exec(codeareadata)

            sys.stdout.close()

            sys.stdout = original_stdout

            output = open('file.txt', 'r').read()

        except Exception as e:
            sys.stdout = original_stdout
            output = e

        # Add the OpenAI code here
        from openai import OpenAI
        OPENAI_API_KEY = "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"
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a job and skill recommender"},
                {"role": "user", "content": codeareadata}
            ]
        )
        
        ai_output = completion.choices[0].message.content

    return render(request, 'index.html', {"code": codeareadata, "output": output, "ai_output": ai_output})
