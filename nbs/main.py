from fasthtml.common import *
# from lucide_fasthtml import Lucide


# Add this near the top of your file, after your imports
DEFAULT_THEME = {
    'theme_color_scheme': 'system',
    'theme_hue': 210,
    'theme_rotate': 0,
    'theme_chroma': 0.89,
    'theme_root_size': 100,
    'theme_button_radius': '--radius-round'
}

# Add this near your DEFAULT_THEME at the top
RADIUS_MAP = {
    0: '--radius-1',
    1: '--radius-2',
    2: '--radius-3',
    3: '--radius-4',
    4: '--radius-round'
}


# Add HighlightJS to your headers
app, rt = fast_app(
    exts='head-support',
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://deufel.github.io/css/css/main.css'),
        # Add HighlightJS with CSS support
        HighlightJS(langs=['css']),
        # Add Tokyo Night theme
        Link(rel='stylesheet',
             href='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/tokyo-night-dark.min.css')
    )
)



def css_preview(session):
    return Div(cls="card outlined margin")(
        Hgroup(
            P("Live CSS", cls="overline"),
            H2("Current Theme CSS"),
            P("This shows the current CSS being applied to the page"),
        ),
        Pre(style="max-width: none; width: 100%;")(
            Code( id="css-preview", hx_get="/theme-css", hx_trigger="theme-update from:body", hx_swap="innerHTML", style=" overflow: hidden;")(
                generate_theme_css(session),
        )),
        Script("""
        (function() {
            // Initial highlight
            hljs.highlightElement(document.querySelector('#css-preview'));

            // Debounced highlight function
            let highlightTimeout;
            function debouncedHighlight() {
                clearTimeout(highlightTimeout);
                highlightTimeout = setTimeout(() => {
                    const codeElement = document.querySelector('#css-preview');
                    if (codeElement) hljs.highlightElement(codeElement);
                }, 50);
            }

            // Listen for content updates
            htmx.on('#css-preview', 'htmx:afterSwap', debouncedHighlight);
        })();
        """)
    )

def generate_theme_css(session):
    """Generate CSS from session theme values"""
    css = [':root {']
    css.append(f'color-scheme: {session["theme_color_scheme"]};')
    css.append(f'--palette-hue: {session["theme_hue"]};')
    css.append(f'--palette-hue-rotate-by: {session["theme_rotate"]};')
    css.append(f'--palette-chroma: {session["theme_chroma"]};')
    css.append(f'font-size: {session["theme_root_size"]}%;')
    css.append(f'--button-border-radius: var({session["theme_button_radius"]});')
    css.append('}')
    return '\n'.join(css)

# Routes

@rt("/theme-css")
def get(session):
    return Code(generate_theme_css(session))

# Modify the post route to handle the numeric radius value
@rt("/theme")
def post(session, color_scheme:int=None, hue:int=None, rotate:int=None,
         chroma:float=None, root_size:int=None, button_radius:int=None):

    # Convert the numeric values to their corresponding strings
    if color_scheme is not None:
        scheme_map = {0: 'light', 1: 'dark'}
        color_scheme = scheme_map[color_scheme]

    if button_radius is not None:
        button_radius = RADIUS_MAP[button_radius]

    # Validation
    if color_scheme and color_scheme not in ['light','dark']: return
    if hue is not None and not (0 <= hue <= 360): return
    if rotate is not None and not (-20 <= rotate <= 20): return
    if chroma is not None and not (0 <= chroma <= 1): return
    if root_size is not None and not (50 <= root_size <= 200): return

    # Store valid values in session
    if color_scheme: session['theme_color_scheme'] = color_scheme
    if hue is not None: session['theme_hue'] = hue
    if rotate is not None: session['theme_rotate'] = rotate
    if chroma is not None: session['theme_chroma'] = chroma
    if root_size is not None: session['theme_root_size'] = root_size
    if button_radius is not None: session['theme_button_radius'] = button_radius

    # Your existing CSS generation code
    css = [':root {']
    if color_scheme: css.append(f'color-scheme: {color_scheme};')
    if hue is not None: css.append(f'--palette-hue: {hue};')
    if rotate is not None: css.append(f'--palette-hue-rotate-by: {rotate};')
    if chroma is not None: css.append(f'--palette-chroma: {chroma};')
    if root_size is not None: css.append(f'font-size: {root_size}%;')
    if button_radius is not None: css.append(f'--button-border-radius: var({button_radius});')
    css.append('}')
    css_text = '\n'.join(css)

    # return Style('\n'.join(css), hx_head="re-eval")

    return (
            Style(css_text, hx_head="re-eval"),
            Script("htmx.trigger(document.body, 'theme-update');")
        )



@rt("/")
def get(session):
    """Main theme configurator page"""
    # Initialize theme settings if not present
    for key, value in DEFAULT_THEME.items():
        session.setdefault(key, value)
    # Initial CSS from session
    initial_css = Style(generate_theme_css(session), hx_head='merge')


    theme_controls = (
        Div(cls="card outlined margin")(
            Hgroup(
                P("Theme Controls", cls="overline"),
                H2("Theme"),
                P("Move the sliders to see the change in the Design System Components"),
            ),

            Div(cls="content")(
                # Color scheme selector
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Theme Mode (Light ↔ Dark)"),
                        Input(
                            type='range',
                            min=0,
                            max=1,
                            step=1,
                            value={'light': 0, 'dark': 1}[session['theme_color_scheme']],
                            name="color_scheme",
                            hx_post="/theme",
                            hx_trigger="change"
                        )
                    )
                ),
                # Button radius selector (now as a range)
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Button Radius (Sharp → Round)"),
                        Input(
                            type='range',
                            min=0,
                            max=4,
                            step=1,
                            value=[k for k, v in RADIUS_MAP.items()
                                    if v == session['theme_button_radius']][0],
                            name="button_radius",
                            hx_post="/theme",
                            hx_trigger="change"
                        )
                    )
                ),
                # Root size control
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Root Size (%) [50, 200]"),
                        Input( type='range', min=50, max=200, value=session['theme_root_size'], name="root_size", hx_post="/theme", hx_trigger="change" )
                    )
                ),
                # Hue control
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Theme Hue [0, 360]"),
                        Input( type='range', min=0, max=360, value=session['theme_hue'], name="hue", hx_post="/theme", hx_trigger="change" )
                    )
                ),
                # Rotation control
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Color Palet Hue Step [-20, 20]"),
                        Input( type='range', min=-20, max=20, value=session['theme_rotate'], name="rotate", hx_post="/theme", hx_trigger="change" )
                    )
                ),
                # Chroma control
                Div(
                    Label(cls="range")(
                        Span(cls="label")("Chroma [0,1]"),
                        Input( type='range', min=0, max=1, value=session['theme_chroma'], step=0.01, name="chroma", hx_post="/theme", hx_trigger="change" )
                    )
                )
            ),

            Div(cls="actions")(
                Button(cls="button")         ("Default"),
                Button(cls="button outlined")("Outlined"),
                Button(cls="button tonal")   ("Tonal"),
                Button(cls="button filled")  ("Filled"),
                Button(cls="button elevated")("Elevated"),
            )
        ),
    )


    # Component preview sections
    preview = (
        # Color Palette
        Div(cls="card outlined margin")(
            Hgroup(
                P("Color Palette"),
                H2("Theme Colors"),
            ),
            Div(cls="flex-wrap padding")(
                *[
                    Div(
                        Style=f"""
                            width: var(--size-8);
                            height: var(--size-8);
                            background: var(--color-{i});
                            border-radius: var(--radius-2);
                            position: relative;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        """
                    )(
                        P(Style=f"color: lch(from var(--color-{i}) calc((50 - l) * infinity) 0 0 )")(i)
                    )
                    for i in range(1, 13)
                ]
            )
        ),



        # CSS Preview card
        css_preview(session)

    )

    return (
            Title("OpenProps UI Theme Previewer"),
            Div(cls="flex-center")(
                initial_css,  # Add the initial CSS here
                Container(hx_ext="head-support")(
                    theme_controls,
                    preview,
                )
            )
        )




serve()
