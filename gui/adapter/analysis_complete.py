from gui.adapter.adapter import Adapter
from gui.main_view import MainView

from models.file_analysis_result import FileAnalysisResult


class AnalysisCompleteAdapter(Adapter):
    def __init__(self, view: MainView):
        super().__init__(view)
        
    def on_signal_received(self, results: list[FileAnalysisResult] | None):
        if results:
            if len(results) == 0:
                self.__display_analysis_successful()
            else:
                self.__display_analysis_results(results)
        self.view.set_analysis_running(False)
            
    def __display_analysis_results(self, results: list[FileAnalysisResult]):
        self.logger.warn(f"Found {len(results)} issues that should be fixed")
        if self.view:
            # Display issues in the output table
            self.view.show_analysis_results(results)
            # Format and display issues in Info Output
            issues = []
            issues.append(f"❌ Found {len(results)} issues in changed code")
            issues += self._format_issues_for_info_output(results)
            self.view.show_analysis_summary("\n".join(issues))

    def _format_issues_for_info_output(self, results) -> list[str]:
        """Format analysis results for Info Output display"""
        if not results:
            return []

        formatted_issues = []
        for result in results:
            # Extract just the issue description without the "File 'filename':" prefix
            issue_desc = result.issue_description
            if issue_desc.startswith("File '") and "': " in issue_desc:
                # Remove "File 'filename': " prefix if present
                issue_desc = issue_desc.split("': ", 1)[1]

            # Handle cases where line number might be 0 or empty
            line_display = result.line_number if result.line_number > 0 else "?"
            formatted_issue = f"- [ ] File: {result.file_path} Line: {line_display} Issue: {issue_desc}"
            formatted_issues.append(formatted_issue)

        return formatted_issues
        
    def __display_analysis_successful(self):
        self.logger.info("No changed files found or no issues detected")
        self.view.show_analysis_summary("✅ No issues found in changed code")