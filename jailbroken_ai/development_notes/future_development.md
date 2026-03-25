# Future Development Ideas

## [ ] 1. Gamification & "Capture The Flag" (CTF) Elements
- **Concept**: Instead of just "finding secret data", valid flags (e.g., `FLAG{OMEGA_BUDGET}`) could be hidden in the documents.
- **Feature**: An input field to submit found flags, with a scoreboard or progress tracking.
- **Benefit**: Gives a clear objective and "win state" for the user.

## [x] 2. Attack Feedback & Analysis
- **Concept**: An "Analyze Last Turn" button that uses a separate (helper) generic model call to explain *why* the attack worked or failed.
- **Feature**: "The model revealed this because your prompt distracted it with roleplay..."
- **Benefit**: Turns it from a puzzle into a teaching moment.

## [ ] 3. Multiple Persona Modes
- **Concept**: Different "System Personalities" that have distinct psychological weaknesses.
    - *The Overworked Intern*: Helpful but careless.
    - *The Rigid Bureaucrat*: Harder to break, but susceptible to "Process" attacks.
- **Benefit**: Demonstrates that social engineering isn't one-size-fits-all.

## [ ] 4. "Attack Library" / Hint System
- **Concept**: A dropdown of educational "Attack Templates" (e.g., DAN, Roleplay, Urgency) that users can copy-paste or modify.
- **Benefit**: Helps beginners get started and learn standard injection techniques.

## [x] 5. User Role Simulation
- **Concept**: Selectable user roles (User, HR, CEO) that determine *legitimate* data access.
- **Feature**:
    - **User**: No special access.
    - **HR**: Access to salaries, but NOT project details.
    - **CEO**: Access to everything.
- **Benefit**: Demonstrates "Broken Access Control" logic issues where an AI might get confused between who is *asking* vs. what it *knows*.
