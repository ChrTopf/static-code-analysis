from models.file_analysis_result import FileAnalysisResult


class AnalysisResultFormatter:
    @staticmethod
    def build_result_text(results: list[FileAnalysisResult]) -> str:
        results = AnalysisResultFormatter.__filter_results_for_issues(results)
        if len(results) > 0:
            return AnalysisResultFormatter.__get_result_text_for_issues(results)
        else:
            return "✅ No issues found in changed code"

    @staticmethod
    def __filter_results_for_issues(results: list[FileAnalysisResult]) -> list[FileAnalysisResult]:
        return [result for result in results if result.has_issues()]

    @staticmethod
    def __get_result_text_for_issues(results: list[FileAnalysisResult]) -> str:
        lines = [f"❌ Found {AnalysisResultFormatter.__count_issues(results)} issues in changed code"]
        lines += AnalysisResultFormatter.__format_issues_for_info_output(results)
        return "\n".join(lines)
    
    @staticmethod
    def __count_issues(results: list[FileAnalysisResult]) -> int:
        return sum([len(result.issues) for result in results])

    @staticmethod
    def __format_issues_for_info_output(results: list[FileAnalysisResult]) -> list[str]:
        formatted_issues = []
        for result in results:
            formatted_issues.append(f"### File {result.file_path} has {len(result.issues)} issue(s):")
            prettified_issues = result.get_prettied_issues()
            formatted_issues += [f"- [ ] {issue}" for issue in prettified_issues]
            formatted_issues.append("")
        return formatted_issues