# Static Code Analysis Lab Report

**Student Name**: [Your Name]  
**Date**: October 29, 2025

## Known Issues Table

| Issue Type                    | Line(s)         | Tool           | Description                                                        | Fix Approach                                              |
| ----------------------------- | --------------- | -------------- | ------------------------------------------------------------------ | --------------------------------------------------------- |
| Mutable default argument      | 6               | Pylint         | `logs=[]` is shared across function calls, causing state pollution | Changed to `logs=None` and initialize inside function     |
| Bare exception clause         | 19-22           | Pylint, Flake8 | `except:` catches all exceptions including system exits            | Changed to `except KeyError:` for specific error handling |
| Security vulnerability        | 41              | Bandit         | `eval()` can execute arbitrary malicious code                      | Removed the dangerous eval() statement completely         |
| Unsafe file handling          | 25-28, 31-34    | Pylint         | Files not properly closed on error                                 | Used `with open()` context manager for automatic cleanup  |
| Old string formatting         | 8, 35           | Pylint         | Using old `%` string formatting instead of modern f-strings        | Replaced with f-strings for better readability            |
| Missing type validation       | 7, 33           | Custom         | No checks for invalid types (int as item name, string as qty)      | Added `isinstance()` checks with proper error logging     |
| Global variable usage         | 10, 26          | Pylint         | Global `stock_data` can lead to unexpected behavior                | Documented global usage; added proper global statement    |
| Missing exception handling    | 25              | Pylint         | `FileNotFoundError` and `JSONDecodeError` not caught               | Added try-except blocks with specific exceptions          |
| Missing logging configuration | -               | Best Practice  | No centralized logging setup                                       | Added `logging.basicConfig()` at module level             |
| Function naming convention    | 6, 18, 24, etc. | Pylint         | camelCase instead of Python's snake_case                           | Changed to `add_item`, `remove_item`, `get_qty`, etc.     |
| Missing docstrings            | All functions   | Pylint         | Functions lack documentation                                       | Added comprehensive docstrings for all functions          |
| Line length violations        | Various         | Flake8         | Lines exceed PEP 8's 79 character limit                            | Broke long lines into multiple lines                      |

## Reflection Questions

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest to fix:**

- String formatting changes (% to f-strings) - simple find and replace
- Removing the `eval()` statement - just delete the line
- Adding docstrings - straightforward documentation
- File handling with `with` statements - standard Python pattern

**Hardest to fix:**

- Mutable default arguments - required understanding of how Python handles default parameters and object references
- Type validation logic - needed to think through all edge cases and decide what should be warnings vs errors
- Proper exception handling - had to research which specific exceptions to catch and how to handle them appropriately
- Function renaming - required updating all function calls throughout the code consistently

The conceptual issues (like mutable defaults) were harder than syntactic ones because they required understanding the underlying problem, not just applying a pattern.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

The tools were generally accurate, but there were a few debatable warnings:

**Example**: Pylint's "too-few-public-methods" warning for classes (if we had any). In functional code like this inventory system, not every module needs classes, so this would be a false positive if flagged.

Another borderline case: Pylint flags the global variable `stock_data` as problematic. While global state can be an issue in larger applications, for a simple script like this, it's an acceptable design choice. The warning is technically correct but not necessarily a "bug" in this context.

### 3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate these tools at multiple stages:

**During Development:**

- Install tools locally and run them before committing code
- Use IDE extensions (like pylint integration in VS Code) for real-time feedback
- Set up pre-commit hooks using tools like `pre-commit` to automatically run checks

**In CI/CD Pipeline:**

- Add static analysis as a required step in GitHub Actions / GitLab CI
- Fail builds if critical security issues (Bandit) are detected
- Generate reports as artifacts for each pull request
- Set quality gates: require a minimum Pylint score (e.g., 8.0/10) to merge

**Team Standards:**

- Establish a shared configuration file (`.pylintrc`, `.flake8`) for consistency
- Review and discuss findings in code reviews
- Gradually increase strictness as code quality improves

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

**Security Improvements:**

- Removed the `eval()` vulnerability that could allow arbitrary code execution
- Proper file handling prevents resource leaks
- Input validation prevents type-related crashes

**Readability Improvements:**

- F-strings make string formatting clearer and more intuitive
- Consistent snake_case naming follows Python conventions
- Docstrings provide clear documentation for each function
- Logging provides better visibility into program behavior

**Robustness Improvements:**

- Specific exception handling prevents silent failures
- Type checking catches invalid inputs early
- The mutable default argument fix prevents subtle state-sharing bugs
- File operations with context managers ensure proper cleanup even on errors

**Maintainability:**

- Well-documented code is easier for others (or future me) to understand
- Consistent style makes the codebase feel cohesive
- Proper error messages help debug issues quickly

The code went from "works on my machine sometimes" to "production-ready with proper error handling and logging."

---

## Files in This Repository

1. `inventory_system.py` - Original buggy code
2. `cleaned_inventory_system.py` - Fixed version with all improvements
3. `pylint_report_clean.txt` - Pylint analysis of cleaned code
4. `bandit_report_clean.txt` - Bandit security analysis of cleaned code
5. `flake8_report_clean.txt` - Flake8 style analysis of cleaned code
6. `README.md` - This file (issue table and reflection)

---

## Summary

Through this lab, I successfully identified and fixed **12+ issues** across security, style, and logic categories. The static analysis tools proved invaluable in catching issues I would have missed through manual review alone. The combination of Pylint (code quality), Bandit (security), and Flake8 (style) provides comprehensive coverage for Python development.

**Key Takeaway**: Static analysis should be a standard part of every Python project to catch issues early, maintain consistency, and improve overall code quality.
