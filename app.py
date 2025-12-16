from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    routine = None

    if request.method == "POST":
        level = request.form["level"]
        team_size = int(request.form["team_size"])
        length = int(request.form["length"])
        focus = request.form["focus"]

        # Difficulty scoring logic
        difficulty_score = 0

        if level == "Beginner":
            difficulty_score += 2
        elif level == "Intermediate":
            difficulty_score += 4
        else:
            difficulty_score += 6

        if team_size >= 15:
            difficulty_score += 2
        elif team_size >= 8:
            difficulty_score += 1

        if focus in ["Tumbling", "Stunts"]:
            difficulty_score += 2
        else:
            difficulty_score += 1

        if difficulty_score > 10:
            difficulty_score = 10

        routine = f"""
📣 LET’S GO CHEER SQUAD! 📣

✨ Routine Details ✨
• Skill Level: {level}
• Team Size: {team_size}
• Routine Length: {length} minutes
• Focus Area: {focus}

🔥 Difficulty Score: {difficulty_score}/10 🔥

🎀 Routine Breakdown 🎀
1. High-energy opening dance + cheer
2. Sharp jumps section (hit those motions!)
3. {focus}-focused feature section
4. Group stunt sequence (clean & confident)
5. Final cheer, pose, and BIG SMILE 😄

💖 Coach Tip:
Practice transitions and timing to keep energy high from start to finish!
"""

    return render_template("index.html", routine=routine)

if __name__ == "__main__":
    app.run(debug=True)
