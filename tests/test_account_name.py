"""账号名校验：批量导入按 JSON 文件名命名，中文文件名要能直接当账号名。

2026-11-26：导入提示写的是「账号名取文件名」，但前端只保留 ASCII、后端 NAME_RE 也拒绝中文，
中文文件名会被静默改成 ck1/accN。这里锁住新的规则：中文、字母、数字、_、- 允许，
点/斜杠/空格/超长拒绝（账号名就是 accounts/<name>/ 目录名）。
"""


def _name_re():
    import server
    return server.NAME_RE


def test_name_re_accepts_unicode_and_safe_chars():
    name_re = _name_re()
    for ok in ("繁昌", "昶20", "用户927057", "ck76", "acc_1-2", "a" * 32):
        assert name_re.fullmatch(ok), ok


def test_name_re_rejects_path_and_space():
    name_re = _name_re()
    for bad in ("../x", "a/b", "a.b", "a b", "", "a" * 33, "a\\b"):
        assert not name_re.fullmatch(bad), bad
