from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# ✅ Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Load College Data
with open("college_data.json", "r", encoding="utf-8") as f:
    college = json.load(f)


@app.route("/")
def home():
    return render_template("index.html")


# ✅ ✅ ✅ SINGLE CLEAN CHAT ROUTE ✅ ✅ ✅
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message", "").lower().strip()

        if not user_msg:
            return jsonify({"reply": "Please type a message."})

        has_fee_word = ("fee" in user_msg) or ("fees" in user_msg)

        # ✅ ✅ ✅ FEES (HIGHEST PRIORITY)
        if has_fee_word and "mba" in user_msg:
            return jsonify({"reply": f"MBA Fees: {college['fees'].get('MBA', 'Not available')}"})

        if has_fee_word and ("btech" in user_msg or "b.tech" in user_msg or "b tech" in user_msg):
            return jsonify({"reply": f"B.Tech Fees: {college['fees'].get('B.Tech', 'Not available')}"})

        if has_fee_word and "mca" in user_msg:
            return jsonify({"reply": f"MCA Fees: {college['fees'].get('MCA', 'Not available')}"})

        if has_fee_word and "mtech" in user_msg:
            return jsonify({"reply": f"M.Tech Fees: {college['fees'].get('M.Tech', 'Not available')}"})

        # ✅ ✅ ✅ BASIC INFO
        if "about" in user_msg or "college" in user_msg:
            return jsonify({"reply": college.get("about", "Not available")})

        if "owner" in user_msg:
            o = college.get("owner", {})
            return jsonify({"reply": f"Owner: {o.get('name')} ({o.get('designation')})"})

        if "principal" in user_msg:
            p = college.get("principal", {})
            return jsonify({"reply": f"Principal: {p.get('name')}"})

        if "location" in user_msg or "address" in user_msg:
            return jsonify({"reply": college.get("location")})

        if "phone" in user_msg or "contact" in user_msg or "email" in user_msg or "contect" in user_msg:
            c = college.get("contact", {})
            return jsonify({
                "reply": f"Phone: {c.get('phone')} | Email: {c.get('email')} | Website: {c.get('website')}"
            })

        # ✅ ✅ ✅ COURSES
        if ("course" in user_msg or "courses" in user_msg) and ("ug" in user_msg or "btech" in user_msg):
            return jsonify({"reply": f"UG Courses: {college['courses'].get('UG', [])}"})

        if ("course" in user_msg or "courses" in user_msg) and ("pg" in user_msg or "mba" in user_msg or "mca" in user_msg or "mtech" in user_msg):
            return jsonify({"reply": f"PG Courses: {college['courses'].get('PG', [])}"})

        if "mba" in user_msg and not has_fee_word:
            return jsonify({"reply": f"PG Courses: {college['courses'].get('PG', [])}"})

        # ✅ ✅ ✅ ADMISSION
        if "admission" in user_msg:
            return jsonify({"reply": college.get("admission", {}).get("process")})

        if "document" in user_msg:
            return jsonify({"reply": f"Required Documents: {college['admission'].get('documents_required')}"})

        # ✅ ✅ ✅ DEPARTMENTS
        if "department" in user_msg:
            return jsonify({"reply": f"Departments: {college.get('departments')}"})

        # ✅ ✅ ✅ APPROVAL
        if "aicte" in user_msg or "approval" in user_msg:
            acc = college.get("accreditation", {})
            return jsonify({"reply": f"Approved By: {acc.get('approved_by')} | Affiliated To: {acc.get('affiliated_to')}"})

        # ✅ ✅ ✅ HOSTEL
        if "hostel" in user_msg:
            return jsonify({"reply": "Hostel Available for Boys & Girls"})

        # ✅ ✅ ✅ PLACEMENT
        if "placement" in user_msg or "package" in user_msg:
            p = college.get("placements", {})
            return jsonify({
                "reply": f"Average Package: {p.get('average_package')} | Highest Package: {p.get('highest_package')} | Companies: {p.get('companies')}"
            })

        # ✅ ✅ ✅ AI FALLBACK
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_msg
        )
        reply = response.output_text

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
