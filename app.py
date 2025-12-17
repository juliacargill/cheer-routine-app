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

def format_time(seconds):
    """
    Returns cheer-friendly time labels (seconds + 8-counts).
    """
    eight_counts = max(1, round(seconds / 15))
    return f"{seconds} sec | {eight_counts}×8"


@app.route("/", methods=["GET", "POST"])
def index():
    routine = None

    if request.method == "POST":
        # --- Read inputs safely ---
        mode = request.form.get("mode", "").strip().lower()
        level = request.form.get("level")
        team_size = int(request.form.get("team_size"))
        length = int(request.form.get("length"))

        # =====================================================
        # GAME DAY MODE (FIXED STRUCTURE)
        # =====================================================
        if mode == "game day":
            routine = (
                "📣 GAME DAY CHEER ROUTINE 📣\n\n"
                f"Team Size: {team_size} athletes\n"
                "Total Length: 3 minutes\n\n"
                "🧭 GAME DAY SECTIONS 🧭\n\n"
                "1️⃣ Band Chant (1:00)\n"
                f"{generate_formation(team_size, 'block')}\n\n"
                "   • Sharp motions, chant with band hits\n\n"
                "2️⃣ Cheer (1:00)\n"
                f"{generate_formation(team_size, 'block')}\n\n"
                "   • Crowd interaction, clean motions\n\n"
                "3️⃣ Fight Song (1:00)\n"
                f"{generate_formation(team_size, 'wide')}\n\n"
                "   • Wide, crowd-facing finish\n\n"
                "💖 Coach Tip:\n"
                "Game day routines should be LOUD, simple, and easy for the crowd to follow!"
            )

        # =====================================================
        # COMPETITION MODE (COACH-CONTROLLED)
        # =====================================================
        else:
            selected_sections = request.form.getlist("sections")

            # Safety fallback
            if not selected_sections:
                selected_sections = ["opening", "ending"]

            total_seconds = length * 60
            section_time = total_seconds // len(selected_sections)

            difficulty = 0
            reasons = []

            # --- Base difficulty ---
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

            routine_blocks = []
            section_number = 1

            for section in selected_sections:
                # ---------- OPENING ----------
                if section == "opening":
                    routine_blocks.append(
                        f"{section_number}️⃣ Opening ({format_time(section_time)})\n"
                        f"{generate_formation(team_size, 'block')}\n"
                    )
                    section_number += 1

                # ---------- JUMPS ----------
                elif section == "jumps":
                    routine_blocks.append(
                        f"{section_number}️⃣ Jumps({format_time(section_time)})\n" 
                        f"{generate_formation(team_size, 'block')}\n"
                    )
                    section_number += 1

                # ---------- TUMBLING ----------
                elif section == "tumbling":
                    routine_blocks.append(
                        f"{section_number}️⃣ Tumbling ({format_time(section_time)})\n" 
                        f"{generate_formation(team_size, 'block')}\n"
                    )
                    difficulty = min(difficulty + 1, 10)
                    reasons.append("Tumbling section included")
                    section_number += 1

                # ---------- STUNTS (PODS OF 4) ----------
                elif section == "stunts":
                    routine_blocks.append(
                        f"{section_number}️⃣ Stunts ({format_time(section_time)})\n"
                        f"{generate_formation(team_size, 'stunts')}\n"
                    )
                    difficulty = min(difficulty + 2, 10)
                    reasons.append("Stunt section included")
                    section_number += 1

                # ---------- PYRAMIDS ----------
                elif section == "pyramids":
                    routine_blocks.append(
                        f"{section_number}️⃣ Pyramids ({format_time(section_time)})\n"
                        f"{generate_formation(team_size, 'pyramid')}\n"
                        "Pyramid plan: Connected stunt groups with clean transitions.\n"
                    )
                    difficulty = min(difficulty + 2, 10)
                    reasons.append("Pyramid section included")
                    section_number += 1

                # ---------- ENDING ----------
                elif section == "ending":
                    routine_blocks.append(
                        f"{section_number}️⃣ Ending ({format_time(section_time)})\n"
                        f"{generate_formation(team_size, 'wide')}\n"
                    )
                    section_number += 1

            routine = (
                "🏆 CUSTOM COMPETITION ROUTINE 🏆\n\n"
                f"Skill Level: {level}\n"
                f"Team Size: {team_size} athletes\n"
                f"Routine Length: {length} minutes\n\n"
                f"🔥 Difficulty Score: {difficulty}/10 🔥\n"
                "Why this score:\n"
                + "\n".join([f"• {r}" for r in reasons]) + "\n\n"
                "🧭 SELECTED ROUTINE SECTIONS 🧭\n\n"
                + "\n".join(routine_blocks) +
                "\n💖 Coach Tip:\n"
                "Build routines around your team’s strengths — not every team needs every section!"
            )

    return render_template("index.html", routine=routine)



if __name__ == "__main__":
    app.run(debug=True)

