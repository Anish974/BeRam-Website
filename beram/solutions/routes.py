from flask import Blueprint, render_template, abort
from beram import SOLUTIONS_DATA # Import shared data

solutions_bp = Blueprint('solutions', __name__)

@solutions_bp.route('/')
def list_solutions():
    """Displays the overview page listing all solutions."""
    # Sort solutions to ensure DCIS appears first
    sorted_solutions = sorted(SOLUTIONS_DATA.values(),
                             key=lambda x: 0 if x.get('slug') == 'dcis' else
                                         (1 if x.get('slug') == 'utms' else 2))

    return render_template('solutions.html',
                           title='Our Solutions',
                           solutions=sorted_solutions)

@solutions_bp.route('/<slug>')
def solution_detail(slug):
    """Displays the detail page for a specific solution."""
    solution = SOLUTIONS_DATA.get(slug)
    if not solution:
        # If the slug doesn't match any key in our data, return 404
        abort(404)

    # Check if this solution has a dedicated page
    if solution.get('has_dedicated_page'):
        # Check if a specific template exists for this solution
        if slug == 'dcis':
            return render_template('dcis_detail.html',
                                  title=f"DCIS: {solution['name']}",
                                  solution=solution)
        elif slug == 'utms':
            return render_template('utms_detail.html',
                                  title=f"UTMS: {solution['name']}",
                                  solution=solution)
        else:
            # For other solutions, use a generic detail template
            return render_template('solution_detail_enhanced.html',
                                  title=f"{solution['name']}",
                                  solution=solution)

    # Default solution detail page
    return render_template('solution_detail.html',
                           title=f"Solution: {solution['name']}",
                           solution=solution)