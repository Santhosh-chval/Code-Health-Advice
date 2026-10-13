import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze as raw_analyze

class MetricsAnalyzer:
    def __init__(self, source_code: str):
        self.source_code = source_code.lstrip('\ufeff').replace('\r\n', '\n')

    def check_syntax(self):
        """Parses source code using AST to catch syntax or compilation errors."""
        try:
            ast.parse(self.source_code)
            return None
        except SyntaxError as e:
            return {
                "line": e.lineno,
                "offset": e.offset,
                "text": e.text.strip() if e.text else "",
                "msg": e.msg
            }

    def get_raw_metrics(self):
        """Calculates raw code metrics (LOC, LLOC, SLOC, Comments)."""
        try:
            raw = raw_analyze(self.source_code)
            return {
                "loc": raw.loc,
                "lloc": raw.lloc,
                "sloc": raw.sloc,
                "comments": raw.comments,
                "blank": raw.blank,
                "comment_percent": round((raw.comments / raw.loc) * 100, 2) if raw.loc > 0 else 0.0
            }
        except Exception:
            lines = self.source_code.splitlines()
            loc = len(lines)
            comments = sum(1 for l in lines if l.strip().startswith('#'))
            sloc = sum(1 for l in lines if l.strip() and not l.strip().startswith('#'))
            return {"loc": loc, "lloc": sloc, "sloc": sloc, "comments": comments, "blank": loc - sloc - comments, "comment_percent": round((comments/loc)*100, 2) if loc > 0 else 0.0}

    def get_cyclomatic_complexity(self):
        """Analyzes cyclomatic complexity and grades (A-F) with robust AST fallback."""
        results = []
        try:
            blocks = cc_visit(self.source_code)
            if blocks:
                for block in blocks:
                    rank = getattr(block, 'rank', 'A')
                    results.append({
                        "Function Name": block.name,
                        "Type": getattr(block, 'letter', 'F'),
                        "Complexity": block.complexity,
                        "Rank": rank
                    })
        except Exception:
            pass

        if not results:
            try:
                tree = ast.parse(self.source_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        comp = 1
                        for sub in ast.walk(node):
                            if isinstance(sub, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.With, ast.AsyncWith, ast.Assert)):
                                comp += 1
                            elif isinstance(sub, ast.BoolOp):
                                comp += len(sub.values) - 1
                        
                        if comp <= 5: rank = 'A'
                        elif comp <= 10: rank = 'B'
                        elif comp <= 20: rank = 'C'
                        elif comp <= 30: rank = 'D'
                        elif comp <= 40: rank = 'E'
                        else: rank = 'F'

                        results.append({
                            "Function Name": node.name,
                            "Type": "F",
                            "Complexity": comp,
                            "Rank": rank
                        })
            except Exception as e:
                return [{"error": str(e)}]

        return results if results else []

    def get_halstead_metrics(self):
        """Calculates Halstead complexity metrics."""
        try:
            h = h_visit(self.source_code)
            return {
                "volume": round(h.total.volume, 2),
                "difficulty": round(h.total.difficulty, 2),
                "effort": round(h.total.effort, 2),
                "bugs": round(h.total.bugs, 4)
            }
        except Exception:
            return {"volume": 0.0, "difficulty": 0.0, "effort": 0.0, "bugs": 0.0}

    def get_maintainability_index(self):
        """Calculates the Maintainability Index (0-100 score)."""
        try:
            score = mi_visit(self.source_code, multi=True)
            return round(score, 2)
        except Exception as e:
            return 0.0

    def analyze_all(self):
        """Runs syntax check and metrics evaluation."""
        syntax_err = self.check_syntax()
        if syntax_err:
            return {"syntax_error": syntax_err}

        raw = self.get_raw_metrics()
        complexity = self.get_cyclomatic_complexity()
        halstead = self.get_halstead_metrics()
        mi = self.get_maintainability_index()
        
        valid_complexities = [b.get("Complexity", 0) for b in complexity if isinstance(b, dict) and "Complexity" in b]
        avg_complexity = sum(valid_complexities) / len(valid_complexities) if valid_complexities else 0

        return {
            "syntax_error": None,
            "raw": raw,
            "complexity_details": complexity,
            "avg_complexity": round(avg_complexity, 2),
            "halstead": halstead,
            "maintainability_index": mi
        }