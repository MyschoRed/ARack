from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from IssueNote.models import MaterialIssue
from Rack.models import PaletteSheet


# Create your views here.
@login_required
def material_issue_list(request):
    all_issues = MaterialIssue.objects.all()
    sheets = PaletteSheet.objects.all()
    ctx = {
        'all_issues': all_issues,
        'sheets': sheets
    }
    return render(request, 'IssueNote/issue_note_list.html', ctx)
