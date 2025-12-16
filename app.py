from flask import Flask, render_template, request

app = Flask(__name__)

def generate_formation(team_size, formation_type):
    """
    Cheer-realistic formation generator.
    - Stunts = pods of 4 (2x2 blocks)
    - Pyramids = connected stunt pods
    - Exact athlete count preserved
    """

    athletes = ["X"] * team_size
    formation_lines = []

    # =========================
    # STUNTS: PODS OF 4
    # =========================
    if formation_type == "stunts":
        pods = [athletes[i:i+4] for i in range(0, len(athletes), 4)]

        pod_visuals = []
        for pod in pods:
            if len(pod) == 4:
                pod_visuals.append([
                    "X X",
                    "X X"
                ])
            else:
                # leftovers (spotters)
                pod_visuals.append([" ".join(pod)])

        pods_per_row = 3  # realistic spacing on 9 mats

        for i in range(0, len(pod_visuals), pods_per_row):
            row_pods = pod_visuals[i:i+pods_per_row]

            max_height = max(len(p) for p in row_pods)
            for line_idx in range(max_height):
                line = []
                for pod in row_pods:
                    if line_idx < len(pod):
                        line.append(pod[line_idx])
                    else:
                        line.append("   ")
                formation_lines.append("     ".join(line).center(36))

            formation_lines.append("")  # space between pod rows

        return "\n".join(formation_lines).strip()

    # =========================
    # PYRAMIDS: CONNECTED PODS
    # =========================
    if formation_type == "pyramid":
        pods = [athletes[i:i+4] for i in range(0, len(athletes), 4)]
        pod_blocks = []

        for pod in pods:
            pod_blocks.append([
                "X X",
                "X X"
            ])

        rows = []
        index = 0
        row_counts = [3, 2, 1]  # pyramid shape

        for count in row_counts:
            row = []
            for _ in range(count):
                if index < len(pod_blocks):
                    row.append(pod_blocks[index])
                    index += 1
            if row:
                rows.append(row)

        for row in rows:
            for line_idx in range(2):
                formation_lines.append(
                    "     ".join(pod[line_idx] for pod in row).center(36)
                )
            formation_lines.append("")

        return "\n".join(formation_lines).strip()

    # =========================
    # BLOCK / WIDE FORMATIONS
    # =========================
    max_per_row = 8 if formation_type == "wide" else 6
    athletes_left = team_size

    while athletes_left > 0:
        count = min(max_per_row, athletes_left)
        athletes_left -= count
        formation_lines.append(
            "   ".join(["X"] * count).center(36)
        )

    return "\n".join(formation_lines)



@app.route("/", methods=["GET", "POST"])
def index():
    routine = None

    if request.method == "POST":
        mode = request.form.get("mode")
        level = request.form.get("level")
        team_size = int(request.form.get("team_size"))
        length = int(request.form.get("length"))

        # =========================
        # GAME DAY MODE (FIXED)
        # =========================
        if mode == "Game Day":
            band_chant = 60
            cheer = 60
            fight_song = 60

            band_visual = generate_formation(team_size, 2)
            cheer_visual = generate_formation(team_size, 3)
            fight_visual = generate_formation(team_size, 1)

            routine = (
                "📣 GAME DAY CHEER ROUTINE 📣\n\n"
                f"Mode: Game Day\n"
                f"Team Size: {team_size} athletes\n"
                "Total Length: 3 minutes\n\n"
                "🧭 GAME DAY SECTIONS 🧭\n\n"
                f"1️⃣ Band Chant (1:00)\n"
                f"{band_visual}\n\n"
                "   • Sharp motions, chant with band hits\n\n"
                f"2️⃣ Cheer (1:00)\n"
                f"{cheer_visual}\n\n"
                "   • Crowd interaction, clean motions, volume\n\n"
                f"3️⃣ Fight Song (1:00)\n"
                f"{fight_visual}\n\n"
                "   • Traditional motions, strong ending pose\n\n"
                "💖 Coach Tip:\n"
                "Game day routines should be LOUD, clean, and easy for the crowd to follow!"
            )

        # =========================
        # COMPETITION MODE
        # =========================
        else:
            total_seconds = length * 60

            opening = int(total_seconds * 0.15)
            jumps = int(total_seconds * 0.20)
            stunts = int(total_seconds * 0.30)
            pyramids = int(total_seconds * 0.20)
            ending = total_seconds - (opening + jumps + stunts + pyramids)

            difficulty = 0
            reasons = []

            if level == "Beginner":
                difficulty += 3
                reasons.append("Beginner skill level")
            elif level == "Intermediate":
                difficulty += 6
                reasons.append("Intermediate skill level")
            else:
                difficulty += 8
                reasons.append("Advanced skill level")

            difficulty += 2
            reasons.append("Competition routine structure")

            difficulty = min(difficulty, 10)

            opening_visual = generate_formation(team_size, "block")
            jumps_visual = generate_formation(team_size, "block")
            stunts_visual = generate_formation(team_size, "stunts")
            pyramids_visual = generate_formation(team_size, "pyramid")
            ending_visual = generate_formation(team_size, "wide")




            if level == "Beginner":
                pyramid_plan = "Simple pyramid with preps and spotters."
            elif level == "Intermediate":
                pyramid_plan = "Two-group pyramid with clean connections."
            else:
                pyramid_plan = "Extended pyramid with connection and controlled dismount."

            safety = []
            if team_size < 10:
                safety.append("⚠️ Small team — pyramids should be minimal.")
            if level == "Beginner":
                safety.append("⚠️ Beginner level — prioritize stability over difficulty.")
            if team_size >= 15:
                safety.append("✔ Team size supports safer multi-group pyramids.")

            routine = (
                "🏆 COMPETITION CHEER ROUTINE 🏆\n\n"
                f"Mode: Competition\n"
                f"Skill Level: {level}\n"
                f"Team Size: {team_size} athletes\n"
                f"Routine Length: {length} minutes\n\n"
                f"🔥 Difficulty Score: {difficulty}/10 🔥\n"
                "Why this score:\n"
                + "\n".join([f"• {r}" for r in reasons]) + "\n\n"
                "🧭 COMPETITION ROUTINE BREAKDOWN 🧭\n\n"
                f"1️⃣ Opening ({opening} sec)\n{opening_visual}\n\n"
                f"2️⃣ Jumps ({jumps} sec)\n{jumps_visual}\n\n"
                f"3️⃣ Stunts ({stunts} sec)\n{stunts_visual}\n\n"
                f"4️⃣ Pyramids ({pyramids} sec)\n{pyramids_visual}\n"
                f"   Pyramid plan: {pyramid_plan}\n\n"
                f"5️⃣ Ending ({ending} sec)\n{ending_visual}\n\n"
                "⚠️ SAFETY NOTES ⚠️\n"
                + ("\n".join(safety) if safety else "• No major safety concerns detected.") +
                "\n\n💖 Coach Tip:\n"
                "Clean transitions and visuals win competition scores!"
            )

    return render_template("index.html", routine=routine)


if __name__ == "__main__":
    app.run(debug=True)

