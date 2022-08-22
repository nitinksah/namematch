# flask imports
from flask import Flask, render_template, request, Response

# Local imports
from utility.text_similarity import similarText
from preprocess.text_preprocessing import ProcessText

# Python imports
from http import HTTPStatus
import json

# Accessing the process_text as an object
process_text = ProcessText()


def exception_check(input_string, text):
    if type(input_string) == float:
        input_string = ""
    if type(text) == float:
        text = ""

    return input_string, text


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def name_match():
    if request.method == "POST":
        input_string = request.form["text1"]
        text = request.form["text2"]

        original_name1 = input_string
        original_name2 = text

        if input_string is None or text is None or len(input_string) == 0 or len(text) == 0:
            raise Exception("Text Field Empty")

        query_string = process_text(input_string)
        search_text = process_text(text)

        tmp = []
        for idx in range(len(query_string)):
            if len(query_string[idx]) == 1:
                continue
            tmp.append(query_string[idx])
        query_string = tmp

        tmp = []
        for idx in range(len(search_text)):
            if len(search_text[idx]) == 1:
                continue
            tmp.append(search_text[idx])
        search_text = tmp

        input_string = " ".join(query_string)
        text = " ".join(search_text)

        input_string, text = exception_check(input_string, text)

        if len(input_string.split(" ")) >= len(text.split(" ")):
            text, input_string = input_string, text

        query_string = [input_string]
        search_text = [text]

        report = similarText(query_string, search_text)

        try:
            score = int(report.trademark_report())
        except Exception as e:
            print("Either of the names are empty or one have single letter present")
            score = 0

        cls = "Accepted" if score >= 65 else "Rejected"

        payload = {
            "input_string": original_name1,
            "text": original_name2,
            "score": score,
            "classification": cls,
            "result": "yes"
            if cls == "Accepted"
            else "no"
        }

        print(payload)

        return render_template("index.html", payload=payload)

    else:
        payload = {
            "input_string": "_",
            "text": "_",
            "score": "_",
            "classification": "_",
            "result": "_"
        }
        return render_template("index.html", payload=payload)


@app.route("/name_match", methods=["OPTIONS", "POST"])
def name_match_api():
    try:
        if request.method == "POST" or request.method == "OPTIONS":
            input_string = request.values["text1"]
            text = request.values["text2"]

            original_name1 = input_string
            original_name2 = text

            if input_string is None or text is None or len(input_string) == 0 or len(text) == 0:
                raise Exception("Text Field Empty")

            query_string = process_text(input_string)
            search_text = process_text(text)

            tmp = []
            for idx in range(len(query_string)):
                if len(query_string[idx]) == 1:
                    continue
                tmp.append(query_string[idx])
            query_string = tmp

            tmp = []
            for idx in range(len(search_text)):
                if len(search_text[idx]) == 1:
                    continue
                tmp.append(search_text[idx])
            search_text = tmp

            input_string = " ".join(query_string)
            text = " ".join(search_text)

            input_string, text = exception_check(input_string, text)

            if len(input_string.split(" ")) >= len(text.split(" ")):
                text, input_string = input_string, text

            query_string = [input_string]
            search_text = [text]

            report = similarText(query_string, search_text)

            try:
                score = int(report.trademark_report())
            except Exception as e:
                print("Either of the names are empty or one have single letter present")
                score = 0

            cls = "Accepted" if score >= 65 else "Rejected"

            payload = json.dumps(
                {
                    "input_string": original_name1,
                    "text": original_name2,
                    "score": score,
                    "classification": cls,
                    "result": "yes"
                    if cls == "Accepted"
                    else "no"
                }
            )

            return Response({payload}, HTTPStatus.OK, mimetype="application/json")

    except Exception as e:
        result = json.dumps({"message": str(e)})
        return Response(result, HTTPStatus.BAD_REQUEST, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
