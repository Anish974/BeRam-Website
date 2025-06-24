from flask import Blueprint, render_template, abort
from beram import PROJECTS_DATA

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
def list_projects():
    return render_template('projects.html', title='Our Projects', projects=PROJECTS_DATA.values())

@projects_bp.route('/<slug>')
def project_detail(slug):
    project = PROJECTS_DATA.get(slug)
    if not project:
        abort(404) # Project not found

    # Check if this project has a dedicated page
    if project.get('has_dedicated_page'):
        # Check for specific templates first
        if slug == 'dcis':
            return render_template('project_dcis.html', title=project['name'], project=project)
        elif slug == 'utms':
            return render_template('project_utms.html', title=project['name'], project=project)

        elif slug == 'vidya-connect':
            return render_template('project_vidya_connect.html', title=project['name'], project=project)
        elif slug == 'vertical-axis-turbine':
            return render_template('project_vertical_axis_turbine.html', title=project['name'], project=project)
        else:
            # Use enhanced template for other projects with dedicated pages
            return render_template('project_detail_enhanced.html', title=project['name'], project=project)

    # Default project detail page
    return render_template('project_detail.html', title=project['name'], project=project)