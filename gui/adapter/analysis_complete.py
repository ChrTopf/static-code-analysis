from gui.adapter.adapter import Adapter
from gui.main_view import MainView
from logger import Logger

from models.file_analysis_result import FileAnalysisResult


class AnalysisCompleteAdapter(Adapter):
    def __init__(self, logger: Logger, view: MainView):
        super().__init__(view)
        self.logger = logger
        
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
            self.view.get_result_section().show_analysis_results(results)
            # Format and display issues in Info Output
            issues = []
            issues.append(f"❌ Found {len(results)} issues in changed code")
            issues += self._format_issues_for_info_output(results)
            self.view.get_result_section().show_analysis_summary("\n".join(issues))

    def _format_issues_for_info_output(self, results: list[FileAnalysisResult]) -> list[str]:
        """Format analysis results for Info Output display"""
        if not results:
            return []

        formatted_issues = []
        for result in results:
            for issue in result.issues:
                formatted_issue = (f"- [ ] "
                                   f"File: {result.file_path} "
                                   f"Line: {issue.line_number} "
                                   f"Issue: {issue.issue_description}")
                formatted_issues.append(formatted_issue)

        return formatted_issues
        
    def __display_analysis_successful(self):
        self.logger.info("No changed files found or no issues detected")
        self.view.get_result_section().show_analysis_summary("✅ No issues found in changed code")