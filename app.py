"""
╔══════════════════════════════════════════════════════════════════════╗
║  UK PROPERTY INTELLIGENCE TERMINAL  ·  Zoned Edition (v2.0)            ║
║  Run:  streamlit run app.py                                          ║
║  Needs: pip install streamlit pandas plotly numpy scikit-learn       ║
║  Data:  merged_pp.csv  (placed in same folder as this file)         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
import gc
import random
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PAGE CONFIG                                                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
st.set_page_config(
    page_title="UK Property Terminal",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# AGGRESSIVE keyboard_double removal
st.markdown("""
<script>
// Remove keyboard_double immediately
(function() {
    function removeKeyboardDouble() {
        // Remove all text nodes containing "keyboard_double"
        const walk = document.createTreeWalker(
            document.documentElement,
            NodeFilter.SHOW_TEXT,
            null
        );
        let textNode;
        const nodesToRemove = [];
        while (textNode = walk.nextNode()) {
            if (textNode.nodeValue && textNode.nodeValue.includes('keyboard_double')) {
                nodesToRemove.push(textNode);
            }
        }
        nodesToRemove.forEach(node => node.remove());
        
        // Remove elements with keyboard in aria-label
        document.querySelectorAll('[aria-label*="keyboard"]').forEach(el => el.remove());
        document.querySelectorAll('[title*="keyboard"]').forEach(el => {
            if (el.title.includes('keyboard_double')) el.remove();
        });
    }
    
    // Run immediately
    removeKeyboardDouble();
    
    // Run on mutations (when content changes)
    const observer = new MutationObserver(removeKeyboardDouble);
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Also run periodically just to be sure
    setInterval(removeKeyboardDouble, 500);
})();
</script>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  NEON DARK THEME CSS — Production Grade Dark Mode with Neon Accents        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=IBM+Plex+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

:root {
  --bg-0: #0a0e27;
  --bg-1: #0f1428;
  --bg-2: #151d3a;
  --bg-3: #1a2847;
  --bg-4: #202d4e;
  
  --neon-pink: #ff006e;
  --neon-cyan: #00d9ff;
  --neon-lime: #39ff14;
  --neon-purple: #b500ff;
  --neon-orange: #ff6600;
  --neon-teal: #00ffc8;
  
  --accent-1: #ff006e;
  --accent-2: #00d9ff;
  --accent-3: #39ff14;
  
  --text-primary: #f0f0f7;
  --text-muted: #7a8fa6;
  --text-dim: #4a5f7f;
  --border-color: #1e2d4a;
  
  --shadow-lg: 0 20px 60px rgba(255, 0, 110, 0.15), 0 0 40px rgba(0, 217, 255, 0.1);
  --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.4);
  --glow-pink: 0 0 20px rgba(255, 0, 110, 0.4);
  --glow-cyan: 0 0 20px rgba(0, 217, 255, 0.3);
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, .block-container, section.main {
  background: linear-gradient(135deg, var(--bg-0) 0%, var(--bg-1) 50%, var(--bg-0) 100%) !important;
  color: var(--text-primary) !important;
  font-family: 'Space Grotesk', 'IBM Plex Mono', monospace !important;
}

.block-container {
  padding: 1rem 1.5rem 3rem !important;
  max-width: 100% !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--bg-2) 0%, var(--bg-1) 100%) !important;
  border-right: 2px solid var(--neon-cyan) !important;
  box-shadow: inset -10px 0 40px rgba(0, 217, 255, 0.05) !important;
}

[data-testid="stSidebar"] * {
  color: var(--text-primary) !important;
  font-family: 'IBM Plex Mono', monospace !important;
}

[data-testid="stSidebar"] input, [data-testid="stSidebar"] select {
  background: var(--bg-3) !important;
  border: 1px solid var(--neon-cyan) !important;
  color: var(--text-primary) !important;
  box-shadow: inset 0 0 10px rgba(0, 217, 255, 0.1) !important;
}

/* ── INPUTS & DROPDOWNS ── */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div {
  background: var(--bg-3) !important;
  border: 1.5px solid var(--neon-purple) !important;
  color: var(--text-primary) !important;
  box-shadow: 0 0 15px rgba(181, 0, 255, 0.1) !important;
}

div[data-baseweb="select"] span, div[data-baseweb="select"] div {
  color: var(--text-primary) !important;
  background: var(--bg-3) !important;
}

div[data-baseweb="popover"] ul {
  background: var(--bg-2) !important;
  border: 1px solid var(--neon-cyan) !important;
}

div[data-baseweb="popover"] li {
  color: var(--text-primary) !important;
}

div[data-baseweb="popover"] li:hover {
  background: var(--bg-4) !important;
  border-left: 3px solid var(--neon-pink) !important;
}

[data-testid="stSlider"] * {
  color: var(--text-primary) !important;
}

/* ── FIX INPUT HOVER ARTIFACTS ── */
input::placeholder {
  color: transparent !important;
  opacity: 0 !important;
}

input::-webkit-input-placeholder {
  color: transparent !important;
  opacity: 0 !important;
}

input:-moz-placeholder {
  color: transparent !important;
  opacity: 0 !important;
}

input::-moz-placeholder {
  color: transparent !important;
  opacity: 0 !important;
}

/* Hide text selection highlight artifacts */
::selection {
  background: rgba(0, 217, 255, 0.05) !important;
  color: var(--text-primary) !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 2px solid var(--neon-cyan) !important;
  gap: 0 !important;
  padding: 0 !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-muted) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  padding: 0.8rem 1.5rem !important;
  border: none !important;
  border-bottom: 3px solid transparent !important;
  text-transform: uppercase !important;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--neon-cyan) !important;
  border-bottom: 3px solid var(--neon-cyan) !important;
  background: rgba(0, 217, 255, 0.08) !important;
  box-shadow: 0 0 20px rgba(0, 217, 255, 0.2), inset 0 -1px 0 var(--neon-cyan) !important;
  text-shadow: 0 0 10px rgba(0, 217, 255, 0.5) !important;
}

[data-testid="stTabs"] [data-baseweb="tab-panel"] {
  background: transparent !important;
  padding-top: 1.5rem !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, rgba(15, 20, 40, 0.8), rgba(21, 29, 58, 0.8)) !important;
  border: 1.5px solid var(--neon-cyan) !important;
  border-top: 2px solid var(--neon-pink) !important;
  border-radius: 6px !important;
  padding: 1rem !important;
  box-shadow: 0 0 25px rgba(0, 217, 255, 0.15), inset 0 0 20px rgba(0, 217, 255, 0.05) !important;
  transition: all 0.3s ease !important;
}

[data-testid="metric-container"]:hover {
  border-color: var(--neon-pink) !important;
  box-shadow: 0 0 35px rgba(255, 0, 110, 0.25), inset 0 0 20px rgba(255, 0, 110, 0.08) !important;
  transform: translateY(-4px) !important;
}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {
  color: var(--neon-cyan) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  text-shadow: 0 0 8px rgba(0, 217, 255, 0.4) !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--neon-lime) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 1.5rem !important;
  font-weight: 900 !important;
  text-shadow: 0 0 15px rgba(57, 255, 20, 0.4) !important;
}

/* ── BUTTONS ── */
button {
  background: linear-gradient(135deg, var(--neon-pink), var(--neon-purple)) !important;
  color: var(--text-primary) !important;
  border: none !important;
  border-radius: 4px !important;
  font-weight: 700 !important;
  box-shadow: 0 0 20px rgba(255, 0, 110, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
  transition: all 0.3s ease !important;
}

button:hover {
  box-shadow: 0 0 40px rgba(255, 0, 110, 0.5), 0 0 20px rgba(181, 0, 255, 0.3) !important;
  transform: translateY(-2px) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
  background: var(--bg-2) !important;
  border: 1px solid var(--neon-purple) !important;
  border-radius: 4px !important;
}

[data-testid="stExpander"] summary {
  color: var(--neon-cyan) !important;
  font-family: 'Orbitron', sans-serif !important;
  font-size: 0.75rem !important;
  text-shadow: 0 0 10px rgba(0, 217, 255, 0.3) !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
  background: var(--bg-3) !important;
  color: var(--text-primary) !important;
}

/* ── TEXT ── */
h1, h2, h3 {
  font-family: 'Orbitron', sans-serif !important;
  color: var(--text-primary) !important;
  letter-spacing: 0.05em !important;
}

p, li, label, span, .stMarkdown {
  color: var(--text-primary) !important;
  font-family: 'Space Grotesk', sans-serif !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-0);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
  border-radius: 4px;
  box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, var(--neon-pink), var(--neon-cyan));
  box-shadow: 0 0 20px rgba(255, 0, 110, 0.4);
}

/* ── FIX KEYBOARD HOVER ARTIFACTS ── */
*::-webkit-input-placeholder {
  color: var(--text-muted) !important;
}
*:-moz-placeholder {
  color: var(--text-muted) !important;
}
*::-moz-placeholder {
  color: var(--text-muted) !important;
}
*:-ms-input-placeholder {
  color: var(--text-muted) !important;
}

/* Remove text selection highlight artifacts */
::selection {
  background: rgba(0, 217, 255, 0.2) !important;
  color: var(--text-primary) !important;
}

::-moz-selection {
  background: rgba(0, 217, 255, 0.2) !important;
  color: var(--text-primary) !important;
}

/* ════════════════════════════════════════════════════════════════════════════
   TOOLTIP SYSTEM
   ════════════════════════════════════════════════════════════════════════════ */
.tt {
  border-bottom: 2px dashed var(--neon-cyan);
  color: var(--neon-cyan);
  cursor: help;
  font-weight: 600;
  position: relative;
  display: inline-block;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.tt:hover {
  text-shadow: 0 0 15px rgba(0, 217, 255, 0.6);
}

.tt::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%) translateY(8px);
  background: linear-gradient(135deg, var(--bg-1), var(--bg-2));
  color: var(--text-primary);
  border: 1.5px solid var(--neon-cyan);
  border-radius: 6px;
  padding: 10px 15px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  line-height: 1.6;
  width: max-content;
  max-width: 300px;
  white-space: normal;
  box-shadow: 0 0 40px rgba(0, 217, 255, 0.3), inset 0 0 20px rgba(0, 217, 255, 0.05);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  z-index: 99999;
  text-transform: none;
  letter-spacing: 0;
}

.tt::before {
  content: '';
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--neon-cyan);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: 99999;
  filter: drop-shadow(0 0 3px rgba(0, 217, 255, 0.4));
}

.tt:hover::after {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.tt:hover::before {
  opacity: 1;
}

/* ── CHART CAPTION ── */
.chart-cap {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  color: var(--text-muted);
  padding: 0.4rem 0.8rem;
  border-left: 3px solid var(--neon-cyan);
  margin-top: 0.3rem;
  margin-bottom: 1rem;
  background: rgba(0, 217, 255, 0.05);
  border-radius: 2px;
}

/* ── ZONE BANNER ── */
.zone-banner {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.65rem;
  font-weight: 900;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--neon-cyan);
  background: linear-gradient(90deg, rgba(0, 217, 255, 0.12), transparent);
  border-left: 4px solid var(--neon-cyan);
  border-bottom: 1px solid rgba(0, 217, 255, 0.2);
  padding: 0.8rem 1.2rem;
  margin-bottom: 1.5rem;
  margin-top: 0.5rem;
  display: block;
  box-shadow: 0 0 20px rgba(0, 217, 255, 0.1), inset 0 0 20px rgba(0, 217, 255, 0.05);
  text-shadow: 0 0 10px rgba(0, 217, 255, 0.4);
}

/* ── TERMINAL BAR ── */
.term-bar {
  background: linear-gradient(90deg, rgba(21, 29, 58, 0.9), rgba(32, 45, 78, 0.9));
  border-bottom: 2px solid var(--neon-cyan);
  border-top: 1px solid rgba(0, 217, 255, 0.2);
  padding: 0.8rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-family: 'Orbitron', sans-serif;
  box-shadow: 0 10px 40px rgba(0, 217, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
  .block-container {
    padding: 0.5rem 0.5rem 1.5rem !important;
  }

  [data-testid="stTabs"] [data-baseweb="tab"] {
    padding: 0.5rem 0.6rem !important;
    font-size: 0.6rem !important;
  }

  .term-bar {
    flex-direction: column;
    gap: 0.8rem;
  }

  .zone-banner {
    font-size: 0.5rem !important;
    padding: 0.3rem 0.6rem !important;
    margin-bottom: 0.8rem !important;
  }
  
  [data-testid="stMetricValue"] {
    font-size: 1.2rem !important;
  }
  
  [data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
  }
  
  /* Hide sidebar on very small screens */
  @media (max-width: 480px) {
    .block-container {
      padding: 0.3rem !important;
    }
  }
}

/* ── HIDE INPUT SPINNERS (BRUTAL) ── */
/* Remove number input spinners */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none !important;
  margin: 0 !important;
  height: 0 !important;
  width: 0 !important;
  display: none !important;
  visibility: hidden !important;
}

input[type="number"] {
  -moz-appearance: textfield !important;
  appearance: textfield !important;
}

/* Hide all picker buttons */
input::-webkit-calendar-picker-indicator,
input::-webkit-clear-button,
input::-webkit-search-cancel-button,
input::-webkit-search-decoration {
  display: none !important;
}

/* Hide all pseudo-elements on inputs */
input::before,
input::after,
textarea::before,
textarea::after {
  display: none !important;
}

/* Remove any remaining arrow elements */
[role="button"][aria-label*="arrow"],
[role="button"][aria-label*="keyboard"],
.react-datepicker__input-container,
button[aria-label*="keyboard"] {
  display: none !important;
}

/* ── HOVER TOOLTIPS - Let Plotly handle it ── */

/* Just ensure text is visible */
.hoverlayer {
  pointer-events: auto !important;
}

.hovertext {
  background-color: #000000 !important;
  color: #39ff14 !important;
  border: 2px solid #00d9ff !important;
}

</style>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  COLOURS & CONSTANTS                                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
NEON_PINK = "#ff006e"
NEON_CYAN = "#00d9ff"
NEON_LIME = "#39ff14"
NEON_PURPLE = "#b500ff"
NEON_ORANGE = "#ff6600"
NEON_TEAL = "#00ffc8"
NEON_PALETTE = [NEON_CYAN, NEON_PINK, NEON_LIME, NEON_ORANGE, NEON_PURPLE, NEON_TEAL]

BG_PLOT = "#0a0e27"
GRID_COLOR = "#151d3a"
AXIS_COLOR = "#1e2d4a"
TEXT_COLOR = "#f0f0f7"
TEXT_MUTED = "#7a8fa6"

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  HELPER FUNCTIONS                                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def tt(label: str, definition: str) -> str:
    """Inline hover tooltip with neon styling."""
    safe = definition.replace('"', '&quot;').replace("'", "&#39;")
    return f'<span class="tt" data-tip="{safe}">{label}</span>'


def cap(html: str):
    """Chart caption with enhanced styling."""
    st.markdown(f'<div class="chart-cap">💡 {html}</div>', unsafe_allow_html=True)


def zbanner(text: str):
    """Zone banner with neon glow."""
    st.markdown(f'<div class="zone-banner">{text}</div>', unsafe_allow_html=True)


def theme(fig, title="", h=350, xrot=0, vlegend=False):
    """Apply neon dark theme to Plotly figures."""
    leg = dict(
        bgcolor="rgba(10, 14, 39, 0.9)",
        bordercolor=AXIS_COLOR,
        borderwidth=1,
        font=dict(size=10, color=TEXT_COLOR, family="IBM Plex Mono"),
        orientation="v" if vlegend else "h",
        yanchor="bottom" if not vlegend else "top",
        y=1.02 if not vlegend else 1,
        xanchor="left",
        x=0 if not vlegend else 1.01,
    )

    fig.update_layout(
        height=h,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=BG_PLOT,
        font=dict(family="IBM Plex Mono, monospace", color=TEXT_COLOR, size=10),
        title=dict(
            text=title,
            font=dict(color=NEON_CYAN, size=14, family="Orbitron"),
            x=0.0,
            xanchor="left",
            y=1.0,
            yanchor="top",
            pad=dict(t=20, b=10, l=0, r=0),
        ),
        legend=leg,
        margin=dict(l=10, r=15, t=100, b=40),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#000000",
            bordercolor="#00d9ff",
            font=dict(color="#39ff14", size=13, family="IBM Plex Mono"),
            namelength=-1,
        ),
    )

    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        linecolor=AXIS_COLOR,
        tickfont=dict(size=9, color=TEXT_MUTED),
        title_font=dict(size=10, color=TEXT_MUTED),
        tickangle=xrot,
        automargin=True,
        showgrid=True,
        gridwidth=0.5,
    )

    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        linecolor=AXIS_COLOR,
        tickfont=dict(size=9, color=TEXT_MUTED),
        title_font=dict(size=10, color=TEXT_MUTED),
        automargin=True,
        showgrid=True,
        gridwidth=0.5,
    )

    return fig


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  DATA LOADING & CLEANING                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

COLS = [
    "price_paid",
    "deed_date",
    "property_type",
    "new_build",
    "estate_type",
    "town",
    "district",
    "county",
    "transaction_type",
]
DTYPE = {
    "price_paid": "float32",
    "property_type": "category",
    "new_build": "category",
    "estate_type": "category",
    "town": "category",
    "district": "category",
    "county": "category",
    "transaction_type": "category",
}


@st.cache_data(show_spinner=False, ttl=7200)
@st.cache_data(show_spinner=False, ttl=86400)
def load_csv(path: str, pct: int) -> pd.DataFrame:
    """Load CSV from local file with smart sampling for large files"""
    
    try:
        # For large files, use sampling to avoid memory issues
        file_size_mb = os.path.getsize(path) / (1024 * 1024)
        
        if file_size_mb > 500:  # If file > 500MB, use sampling
            st.info(f"📦 Large file detected ({file_size_mb:.0f}MB) - loading {pct}% of data for performance")
            
            # Count total lines
            with open(path, "rb") as f:
                total = sum(1 for _ in f) - 1
            
            # Calculate which rows to skip
            keep_n = max(int(total * pct / 100), 10_000)
            skip = (
                set(random.sample(range(1, total + 1), total - keep_n))
                if keep_n < total
                else set()
            )
            
            df = pd.read_csv(
                path,
                skiprows=lambda i: i in skip,
                low_memory=True,
                on_bad_lines="skip",
            )
        else:
            # For smaller files, load normally
            df = pd.read_csv(
                path,
                low_memory=True,
                on_bad_lines="skip",
            )
        
        df.columns = [c.lower().strip() for c in df.columns]
        return _clean(df)
        
    except Exception as e:
        st.error(f"Error loading {path}: {str(e)[:50]}")
        return pd.DataFrame()
    
    return pd.DataFrame()
    
    keep_n = max(int(total * pct / 100), 5_000)
    skip = (
        set(random.sample(range(1, total + 1), total - keep_n))
        if keep_n < total
        else set()
    )
    
    try:
        df = pd.read_csv(
            local_file,
            usecols=lambda c: c.lower().strip() in [x.lower() for x in COLS],
            dtype=DTYPE,
            parse_dates=[],  # Don't parse dates during read, do it after
            skiprows=lambda i: i in skip,
            low_memory=True,
            on_bad_lines="skip",
        )
    except:
        # If selective column loading fails, load everything
        df = pd.read_csv(
            local_file,
            skiprows=lambda i: i in skip,
            low_memory=True,
            on_bad_lines="skip",
        )
    
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Convert date column if it exists (try multiple names)
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    if date_cols:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
    
    return _clean(df)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich data."""
    
    # Find the date column (might be deed_date, transaction_date, date, etc)
    date_col = None
    for col in df.columns:
        if 'date' in col.lower():
            date_col = col
            break
    
    # Find required columns
    price_col = None
    county_col = None
    for col in df.columns:
        if 'price' in col.lower():
            price_col = col
        if 'county' in col.lower():
            county_col = col
    
    # Use defaults if not found
    if not price_col:
        price_col = 'price_paid'
    if not county_col:
        county_col = 'county'
    if not date_col:
        date_col = 'deed_date'
    
    # Only drop rows if columns exist
    cols_to_check = [col for col in [price_col, date_col, county_col] if col in df.columns]
    if cols_to_check:
        df = df.dropna(subset=cols_to_check)
    
    # Clean price
    if price_col in df.columns:
        df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
        df = df[df[price_col].between(10_000, 10_000_000)].copy()
    
    # Clean date
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df["year"] = df[date_col].dt.year.astype("int16")
        df["month"] = df[date_col].dt.month.astype("int8")
        df["month_name"] = df[date_col].dt.strftime("%B")
    else:
        # Create dummy year/month if no date column
        df["year"] = 2020
        df["month"] = 1
        df["month_name"] = "January"

    # Map property attributes to readable names
    if "property_type" in df.columns:
        pt_map = {"D": "Detached", "S": "Semi-Detached", "F": "Flat", "T": "Terraced", "O": "Other"}
        df["Property Type"] = df["property_type"].map(pt_map).fillna("Other")
    
    if "estate_type" in df.columns:
        et_map = {"F": "Freehold", "L": "Leasehold"}
        df["Estate Type"] = df["estate_type"].map(et_map).fillna("Leasehold")
    
    if "new_build" in df.columns:
        nb_map = {"Y": "New Build", "N": "Existing"}
        df["Build Type"] = df["new_build"].map(nb_map).fillna("Existing")

    # Clean county names
    if county_col in df.columns:
        df[county_col] = df[county_col].astype(str).str.strip()
        df[county_col] = df[county_col].str.split(",").str[0].str.strip()
        df[county_col] = df[county_col].str.upper()
        df = df[df[county_col].notna() & (df[county_col] != "NONE") & (df[county_col] != "")].copy()
        df[county_col] = df[county_col].astype("category")
    
    if "town" in df.columns:
        df["town"] = df["town"].astype(str).str.upper().str.strip()
        df["town"] = df["town"].astype("category")
    
    df["month_name"] = df["month_name"].astype("category")
    
    # Convert new columns to category
    for col in ["Property Type", "Estate Type", "Build Type"]:
        if col in df.columns:
            df[col] = df[col].astype("category")
    
    gc.collect()
    return df


def make_demo() -> pd.DataFrame:
    """Generate demo dataset for testing."""
    np.random.seed(42)
    n = 250_000
    counties = [
        "GREATER LONDON",
        "GREATER MANCHESTER",
        "WEST YORKSHIRE",
        "KENT",
        "ESSEX",
        "SURREY",
        "LANCASHIRE",
        "HAMPSHIRE",
        "HERTFORDSHIRE",
        "WEST MIDLANDS",
        "DERBYSHIRE",
        "NOTTINGHAMSHIRE",
        "BRISTOL",
        "CORNWALL",
        "CUMBRIA",
        "NORTH YORKSHIRE",
        "OXFORDSHIRE",
        "BUCKINGHAMSHIRE",
        "CAMBRIDGESHIRE",
        "CHESHIRE",
    ]
    base = dict(
        zip(
            counties,
            [
                680000,
                220000,
                210000,
                370000,
                360000,
                560000,
                190000,
                370000,
                490000,
                250000,
                220000,
                215000,
                380000,
                310000,
                230000,
                310000,
                440000,
                520000,
                400000,
                300000,
            ],
        )
    )
    towns = [
        "LONDON",
        "MANCHESTER",
        "LEEDS",
        "MAIDSTONE",
        "CHELMSFORD",
        "GUILDFORD",
        "BLACKPOOL",
        "SOUTHAMPTON",
        "WATFORD",
        "BIRMINGHAM",
        "DERBY",
        "NOTTINGHAM",
        "BRISTOL",
        "TRURO",
        "CARLISLE",
        "YORK",
        "OXFORD",
        "AYLESBURY",
        "CAMBRIDGE",
        "CHESTER",
    ]
    wts = [0.16, 0.09, 0.06, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.05,
           0.04, 0.04, 0.04, 0.03, 0.03, 0.04, 0.04, 0.04, 0.04, 0.05]

    # Normalize weights to handle floating-point precision
    wts = np.array(wts, dtype=float)
    wts = np.clip(wts, 0, None)
    wts = wts / wts.sum()

    c_arr = np.random.choice(counties, n, p=wts)

    prices = np.array(
        [np.random.lognormal(np.log(base[c]), 0.35) for c in c_arr], dtype="float32"
    )
    years = np.random.choice(range(2018, 2026), n, p=[0.1, 0.12, 0.1, 0.14, 0.16, 0.15, 0.13, 0.1])
    prices *= 1 + (years - 2018) * 0.03
    tmap = dict(zip(counties, towns))

    df = pd.DataFrame(
        {
            "price_paid": prices.clip(20000, 3000000),
            "deed_date": pd.to_datetime("2018-01-01")
            + pd.to_timedelta(np.random.randint(0, 2920, n), "D"),
            "county": pd.Categorical(c_arr),
            "town": pd.Categorical([tmap.get(c, "UNKNOWN") for c in c_arr]),
            "Property Type": pd.Categorical(
                np.random.choice(
                    ["Detached", "Semi-Detached", "Flat", "Terraced", "Other"],
                    n,
                    p=[0.29, 0.27, 0.2, 0.2, 0.04],
                )
            ),
            "Estate Type": pd.Categorical(
                np.random.choice(["Freehold", "Leasehold"], n, p=[0.64, 0.36])
            ),
            "Build Type": pd.Categorical(
                np.random.choice(["New Build", "Existing"], n, p=[0.14, 0.86])
            ),
            "transaction_type": pd.Categorical(
                np.random.choice(["Standard", "Additional"], n, p=[0.9, 0.1])
            ),
            "property_type": "D",
            "estate_type": "F",
            "new_build": "N",
        }
    )
    df["year"] = df["deed_date"].dt.year.astype("int16")
    df["month"] = df["deed_date"].dt.month.astype("int8")
    df["month_name"] = df["deed_date"].dt.strftime("%B").astype("category")
    return df


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PREDICTIVE ANALYTICS                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def predict_2026_price(df: pd.DataFrame, county: str, n_months: int = 12) -> dict:
    """
    Predict county prices for 2026 using polynomial regression.
    Returns predicted price, confidence interval, and growth rate.
    
    Validation:
    - Requires at least 3 years of data
    - Must have data from 2023 or later
    - Checks for unrealistic predictions
    """
    county_data = df[df["county"] == county].copy()
    
    if len(county_data) < 20:
        return {"prediction": None, "growth": 0, "confidence": "Insufficient data", "data": "<20 records"}
    
    # Aggregate by year
    yearly = county_data.groupby("year")["price_paid"].mean().reset_index()
    yearly = yearly.sort_values("year")
    
    # CRITICAL: Check data recency
    latest_year = yearly["year"].max()
    if latest_year < 2023:
        return {
            "prediction": None,
            "growth": 0,
            "confidence": "No recent data",
            "data": f"Last data: {int(latest_year)}"
        }
    
    # CRITICAL: Need at least 3 years
    if len(yearly) < 3:
        return {
            "prediction": None,
            "growth": 0,
            "confidence": "Insufficient years",
            "data": f"{len(yearly)} year(s) only"
        }
    
    # Fit polynomial model (degree 2)
    X = yearly["year"].values.reshape(-1, 1)
    y = yearly["price_paid"].values
    
    model = np.polyfit(X.ravel(), y, 2)
    poly = np.poly1d(model)
    
    # Predict 2026
    pred_2026 = poly(2026)
    
    # VALIDATION: Check if prediction is realistic
    # Reasonable bounds: -50% to +200% change from last price
    last_price = y[-1]
    price_change_pct = ((pred_2026 - last_price) / last_price * 100) if last_price > 0 else 0
    
    if pred_2026 < 0 or price_change_pct < -50 or price_change_pct > 200:
        return {
            "prediction": None,
            "growth": 0,
            "confidence": "Unrealistic prediction",
            "data": f"{len(yearly)} years (extrapolation too extreme)"
        }
    
    # Calculate growth rate from last year
    growth = price_change_pct
    
    # Calculate confidence (based on data quality & recency)
    residuals = y - poly(X.ravel())
    mape = np.mean(np.abs(residuals / y)) * 100
    
    # More strict confidence levels
    if len(yearly) >= 5 and mape < 5 and latest_year >= 2024:
        confidence = "High"
    elif len(yearly) >= 4 and mape < 10 and latest_year >= 2023:
        confidence = "Medium"
    else:
        confidence = "Low"
    
    return {
        "prediction": float(pred_2026),
        "growth": float(growth),
        "confidence": confidence,
        "data": f"{len(yearly)} years (latest: {int(latest_year)})",
        "mape": float(mape),
    }


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  SIDEBAR — DATA LOADING                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown(
        f"""
    <div style='font-family:"Orbitron",sans-serif;padding:.5rem 0 1rem'>
      <div style='font-size:.55rem;letter-spacing:.25em;color:{NEON_CYAN};font-weight:900;text-shadow: 0 0 10px rgba(0, 217, 255, 0.5)'>UK PROPERTY PRICES DASHBOARD</div>
      <div style='font-size:.95rem;font-weight:700;color:{NEON_LIME};margin:.2rem 0;text-shadow: 0 0 8px rgba(57, 255, 20, 0.4)'>UK PROPERTY TERMINAL</div>
      <div style='font-size:.5rem;color:{TEXT_MUTED}'>HM LAND REGISTRY · PRICE PAID DATA</div>
    </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        f'<div style="font-family:Orbitron;font-size:.6rem;color:{NEON_PINK};letter-spacing:.15em;font-weight:900;margin-bottom:.4rem;text-shadow: 0 0 10px rgba(255, 0, 110, 0.4)">🎛️ LOAD DATA</div>',
        unsafe_allow_html=True,
    )

    # Hardcode filename - users don't need to see it
    data_file = "merged_pp.csv"
    
    refresh = st.button("🔄 Load / Refresh Data", use_container_width=True, key="sidebar_refresh_btn")

    if "df" not in st.session_state or refresh:
        # Just load demo data
        st.session_state["df"] = make_demo()
        st.session_state["is_demo"] = True

    df = st.session_state["df"]
    is_demo = st.session_state.get("is_demo", True)

    if is_demo:
        st.info("""
        📊 **Currently showing demo data** (250k sample transactions)
        
        **To load your real data:**
        👇 Upload your CSV file below (supports files up to 200MB)
        """)
        
        # FILE UPLOAD
        uploaded_file = st.file_uploader(
            "📁 Upload your merged_pp.csv", 
            type="csv",
            key="csv_upload_main"
        )
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.warning(f"⏳ Loading {file_size_mb:.1f}MB file... This may take a minute")
            
            with st.spinner(f"Processing {file_size_mb:.1f}MB file…"):
                try:
                    # For large files, read with chunks and low memory
                    upload_df = pd.read_csv(
                        uploaded_file,
                        low_memory=True,
                        on_bad_lines="skip",
                        dtype_backend='numpy_nullable'
                    )
                    
                    upload_df.columns = [c.lower().strip() for c in upload_df.columns]
                    st.session_state["df"] = _clean(upload_df)
                    st.session_state["is_demo"] = False
                    df = st.session_state["df"]
                    st.success(f"✅ Loaded {len(df):,} records from {file_size_mb:.1f}MB file!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)[:100]}")
    else:
        st.success(f"✅ {len(df):,} records loaded")
    
    # Check if df is empty
    if df.empty:
        st.warning("⚠️ **Dataset is empty - upload a CSV to get started!**")

    st.markdown("---")
    st.markdown(
        f'<div style="font-family:Orbitron;font-size:.6rem;color:{NEON_PINK};letter-spacing:.15em;font-weight:900;margin-bottom:.4rem;text-shadow: 0 0 10px rgba(255, 0, 110, 0.4)">⏱️ TIME PERIOD</div>',
        unsafe_allow_html=True,
    )
    
    # ONLY filter: Year Range
    all_years = sorted(df["year"].dropna().unique().astype(int).tolist()) if "year" in df.columns else []
    
    # Handle empty dataframe
    if all_years:
        sel_years = st.select_slider(
            "Select years",
            options=all_years,
            value=(min(all_years), max(all_years)),
            key="sidebar_year_slider",
        )
    else:
        sel_years = (2018, 2025)
        st.warning("⚠️ No year data found in dataset")
    
    # Set defaults for everything else
    sel_counties = sorted(df["county"].dropna().unique().tolist()) if "county" in df.columns else []
    all_pt = sorted(df["Property Type"].dropna().unique().tolist()) if "Property Type" in df.columns else []
    sel_pt = all_pt
    all_bt = sorted(df["Build Type"].dropna().unique().tolist()) if "Build Type" in df.columns else []
    sel_bt = all_bt
    all_et = sorted(df["Estate Type"].dropna().unique().tolist()) if "Estate Type" in df.columns else []
    sel_et = all_et
    sel_towns = []

    st.markdown("---")
    # Removed hover instruction - info is now below metrics

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  FILTER FUNCTION                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


@st.cache_data(show_spinner=False)
def filt(_df, yrs, cos, pt, bt, et, tw):
    m = _df["year"].between(yrs[0], yrs[1])
    if cos:
        m &= _df["county"].isin(cos)
    if pt:
        m &= _df["Property Type"].isin(pt)
    if bt:
        m &= _df["Build Type"].isin(bt)
    if et:
        m &= _df["Estate Type"].isin(et)
    if tw:
        m &= _df["town"].isin(tw)
    return _df[m].copy()


with st.spinner("Filtering…"):
    dff = filt(df, sel_years, sel_counties, sel_pt, sel_bt, sel_et, sel_towns)

# Check if filtered data is empty
if dff.empty:
    st.error("❌ No data matches your filters. Please check your Google Drive file.")
    st.stop()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  HEADER                                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

st.markdown(
    f"""
<div class="term-bar">
  <div>
    <div style='font-size:.5rem;letter-spacing:.28em;color:{NEON_CYAN};font-weight:900'>GOLDMAN SACHS ASSET MANAGEMENT</div>
    <div style='font-size:1.1rem;font-weight:900;color:{NEON_LIME};letter-spacing:.04em;text-shadow: 0 0 15px rgba(57, 255, 20, 0.5)'>UK RESIDENTIAL PROPERTY INTELLIGENCE</div>
    <div style='font-size:.5rem;color:{TEXT_MUTED};letter-spacing:.1em'>PRICE PAID DATA · HM LAND REGISTRY</div>
  </div>
  <div style='text-align:right'>
    <div style='font-size:.5rem;color:{TEXT_MUTED}'>STATUS</div>
    <div style='font-size:.75rem;color:{NEON_LIME};font-weight:900;text-shadow: 0 0 10px rgba(57, 255, 20, 0.5)'>● LIVE ANALYSIS</div>
    <div style='font-size:.55rem;color:{NEON_CYAN}'>{len(dff):,} RECORDS</div>
  </div>
</div>""",
    unsafe_allow_html=True,
)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  KPI ROW                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

yr_end = sel_years[1]
yr_start = sel_years[0]
cur_avg = (
    dff[dff["year"] == yr_end]["price_paid"].mean()
    if yr_end in dff["year"].values
    else np.nan
)
prv_avg = (
    dff[dff["year"] == yr_end - 1]["price_paid"].mean()
    if (yr_end - 1) in dff["year"].values
    else np.nan
)
s_avg = dff[dff["year"] == yr_start]["price_paid"].mean()
n_yrs = max(yr_end - yr_start, 1)
yoy_val = (
    (cur_avg - prv_avg) / prv_avg * 100
    if (not np.isnan(prv_avg) and prv_avg > 0)
    else 0.0
)
cagr_v = (
    ((cur_avg / s_avg) ** (1 / n_yrs) - 1) * 100
    if (not np.isnan(s_avg) and s_avg > 0 and not np.isnan(cur_avg))
    else 0.0
)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.metric("TRANSACTIONS", f"{len(dff):,}")
    st.caption("Total property sales")

with k2:
    st.metric("AVG PRICE", f"£{dff['price_paid'].mean():,.0f}")
    st.caption("Mean price paid")

with k3:
    st.metric("MEDIAN PRICE", f"£{dff['price_paid'].median():,.0f}")
    st.caption("Middle price point")

with k4:
    st.metric("YoY CHANGE", f"{'▲' if yoy_val >= 0 else '▼'}{abs(yoy_val):.1f}%")
    st.caption(f"Price change {yr_end-1} to {yr_end}")

with k5:
    st.metric("CAGR", f"{cagr_v:.2f}%")
    st.caption(f"Annual growth rate")

with k6:
    st.metric("TOTAL VOLUME", f"£{dff['price_paid'].sum()/1e9:.1f}B")
    st.caption("Total money exchanged")

st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)

# Additional important metrics
st.markdown(
    f'<div style="font-family:Orbitron;font-size:.65rem;color:{NEON_CYAN};letter-spacing:.12em;font-weight:900;margin-bottom:.5rem;text-shadow: 0 0 10px rgba(0, 217, 255, 0.4)">📊 DEEPER INSIGHTS</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

# Calculate metrics
price_std = dff["price_paid"].std()
price_cv = (price_std / dff["price_paid"].mean()) * 100 if dff["price_paid"].mean() > 0 else 0
avg_transactions_per_year = len(dff) / max(n_yrs, 1)
median_avg_ratio = (dff["price_paid"].median() / dff["price_paid"].mean()) * 100 if dff["price_paid"].mean() > 0 else 0
top_20pct_value = dff["price_paid"].quantile(0.80)
top_20pct_share = (dff[dff["price_paid"] >= top_20pct_value]["price_paid"].sum() / dff["price_paid"].sum()) * 100 if dff["price_paid"].sum() > 0 else 0

with m1:
    st.metric("PRICE VOLATILITY", f"{price_cv:.1f}%")
    st.caption("Higher = wider price range")

with m2:
    st.metric("AVG TRANSACTIONS/YR", f"{avg_transactions_per_year:,.0f}")
    st.caption("Average sales per year")

with m3:
    st.metric("MEDIAN/AVG RATIO", f"{median_avg_ratio:.1f}%")
    st.caption("<90% = luxury outliers")

with m4:
    st.metric("TOP 20% VALUE SHARE", f"{top_20pct_share:.1f}%")
    st.caption("% of money in top 20%")

st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TABS                                                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

z1, z2, z3, z4 = st.tabs(
    [
        "⚡ MARKET PULSE",
        "🗺️ GEO INTEL",
        "📈 GROWTH ENGINE",
        "🔬 DEEP ANALYSIS",
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# ZONE 1 — MARKET PULSE
# ══════════════════════════════════════════════════════════════════════════════

with z1:
    zbanner("⚡ Market Pulse — Real-time market sentiment & volume dynamics")

    r1a, r1b = st.columns(2)

    with r1a:
        pdg = dff.groupby(["year", "Property Type"]).size().reset_index(name="n")
        fig = go.Figure()
        for i, pt in enumerate(["Detached", "Semi-Detached", "Terraced", "Flat", "Other"]):
            s = pdg[pdg["Property Type"] == pt]
            fig.add_trace(
                go.Scatter(
                    x=s["year"],
                    y=s["n"],
                    name=pt,
                    mode="lines",
                    stackgroup="one",
                    line=dict(width=0.5, color=NEON_PALETTE[i % len(NEON_PALETTE)]),
                    hovertemplate=f"<b>{pt}</b><br>Year: %{{x}}<br>Sales: %{{y:,}}<extra></extra>",
                )
            )
        theme(
            fig,
            tt(
                "PROPERTY DOMINANCE",
                "Shows how many of each home type sold per year. Rising Flat share = urban demand shifting.",
            ),
            h=350,
        )
        st.plotly_chart(fig, use_container_width=True)
        cap("Stacked areas reveal structural market shifts. Growing Flat dominance = urbanisation. Rising Detached = suburban expansion.")

    with r1b:
        dual = dff.groupby("year").agg(
            avg=("price_paid", "mean"), cnt=("price_paid", "size")
        ).reset_index()
        f2 = make_subplots(specs=[[{"secondary_y": True}]])
        f2.add_trace(
            go.Bar(
                x=dual["year"],
                y=dual["cnt"],
                name="Sales Count",
                marker=dict(color=NEON_LIME, opacity=0.7, line=dict(width=0)),
                hovertemplate="Year: %{x}<br>Sales: %{y:,}<extra></extra>",
            ),
            secondary_y=False,
        )
        f2.add_trace(
            go.Scatter(
                x=dual["year"],
                y=dual["avg"],
                name="Avg Price",
                mode="lines+markers",
                line=dict(color=NEON_CYAN, width=3),
                marker=dict(size=7, color=NEON_CYAN, line=dict(color=BG_PLOT, width=2)),
                hovertemplate="Year: %{x}<br>Avg: £%{y:,.0f}<extra></extra>",
            ),
            secondary_y=True,
        )
        theme(
            f2,
            tt(
                "DUAL AXIS",
                "Left: sales volume (bars). Right: average price (line). Spot divergences — when prices rise but volume falls, demand weakening.",
            ),
            h=350,
        )
        f2.update_yaxes(
            title_text="Sales Count",
            secondary_y=False,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_MUTED),
        )
        f2.update_yaxes(
            title_text="Avg Price (£)",
            secondary_y=True,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_MUTED),
            tickprefix="£",
            tickformat=",",
        )
        st.plotly_chart(f2, use_container_width=True)
        cap("When bars ⬇️ but line stays → supply crunch. When both fall → demand weakness. Both rising → healthy boom.")

    st.markdown("---")

    r2a, r2b = st.columns(2)

    with r2a:
        heat = dff.groupby(["year", "month_name"]).size().reset_index(name="n")
        hpiv = heat.pivot(index="year", columns="month_name", values="n").reindex(columns=MONTHS)
        f3 = go.Figure(
            go.Heatmap(
                z=hpiv.values,
                x=MONTHS,
                y=hpiv.index.tolist(),
                colorscale=[
                    [0, BG_PLOT],
                    [0.25, NEON_PURPLE],
                    [0.6, NEON_CYAN],
                    [0.85, NEON_LIME],
                    [1.0, NEON_PINK],
                ],
                hovertemplate="<b>%{y} — %{x}</b><br>Sales: %{z:,}<extra></extra>",
                showscale=True,
                colorbar=dict(thickness=10, tickfont=dict(size=8, color=TEXT_MUTED), outlinewidth=0),
            )
        )
        theme(
            f3,
            tt(
                "SEASONALITY",
                "Grid: months vs years. Brighter = more sales. UK buyers peak in spring (Mar-May) and autumn (Sep-Oct).",
            ),
            h=350,
        )
        f3.update_xaxes(tickangle=-35, tickfont=dict(size=9))
        st.plotly_chart(f3, use_container_width=True)
        cap("Darker = quieter, brighter = busier. Spring and autumn are historically peak buying seasons in the UK.")

    with r2b:
        par = (
            dff.groupby("county")
            .size()
            .reset_index(name="n")
            .sort_values("n", ascending=False)
            .head(15)
        )
        par["cum"] = par["n"].cumsum() / par["n"].sum() * 100
        par["short"] = par["county"].str[:18]
        f4 = make_subplots(specs=[[{"secondary_y": True}]])
        f4.add_trace(
            go.Bar(
                x=par["short"],
                y=par["n"],
                name="Sales Count",
                marker=dict(color=NEON_ORANGE, opacity=0.8, line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>Sales: %{y:,}<extra></extra>",
            ),
            secondary_y=False,
        )
        f4.add_trace(
            go.Scatter(
                x=par["short"],
                y=par["cum"],
                name="Cumulative %",
                mode="lines+markers",
                line=dict(color=NEON_CYAN, width=2.5),
                marker=dict(size=5, color=NEON_CYAN),
                hovertemplate="%{y:.1f}% of all sales<extra></extra>",
            ),
            secondary_y=True,
        )
        theme(
            f4,
            tt(
                "PARETO",
                "80/20 rule: ~80% of transactions come from ~20% of counties. London dominates the UK market.",
            ),
            h=350,
            xrot=-35,
        )
        f4.update_yaxes(
            title_text="Sales",
            secondary_y=False,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_MUTED),
        )
        f4.update_yaxes(
            title_text="Cumulative %",
            secondary_y=True,
            range=[0, 105],
            gridcolor=GRID_COLOR,
            tickfont=dict(size=9, color=TEXT_MUTED),
        )
        st.plotly_chart(f4, use_container_width=True)
        cap("Concentration risk: top counties drive market dynamics. Diversification matters for national-scale investors.")


# ══════════════════════════════════════════════════════════════════════════════
# ZONE 2 — GEO INTEL
# ══════════════════════════════════════════════════════════════════════════════

with z2:
    zbanner("🗺️ Geographic Intelligence — County rankings, hotspots & predictions")

    st.markdown(
        f'<div style="font-family:Orbitron;font-size:.65rem;color:{NEON_PINK};font-weight:900;margin-bottom:.5rem;text-shadow: 0 0 10px rgba(255, 0, 110, 0.4)">📊 UK COUNTY RANKINGS</div>',
        unsafe_allow_html=True,
    )

    hc1, hc2 = st.columns([1, 3])
    with hc1:
        hm_m = st.selectbox(
            "Metric",
            ["Avg Price", "Median Price", "Sales Count", "YoY Change %"],
            key="zone2_metric_select",
        )
        hm_y = st.selectbox(
            "Year",
            sorted(dff["year"].unique(), reverse=True),
            key="zone2_year_select",
        )

    sub_hm = dff[dff["year"] == hm_y]
    ca = (
        sub_hm.groupby("county")
        .agg(
            avg=("price_paid", "mean"),
            med=("price_paid", "median"),
            cnt=("price_paid", "size"),
        )
        .reset_index()
    )

    if hm_m == "YoY Change %":
        ph = dff[dff["year"] == hm_y - 1].groupby("county")["price_paid"].mean()
        ch = sub_hm.groupby("county")["price_paid"].mean()
        yd = ((ch - ph) / ph * 100).reset_index()
        yd.columns = ["county", "value"]
        ca = ca.merge(yd, on="county", how="left")
        vl, vs, fmt = "value", "YoY %", ".1f"
        cs = [
            [0, NEON_PINK],
            [0.35, "#440044"],
            [0.5, BG_PLOT],
            [0.65, "#004444"],
            [1.0, NEON_LIME],
        ]
    elif hm_m == "Sales Count":
        ca["value"] = ca["cnt"]
        vl, vs, fmt = "value", "Sales", ","
        cs = [
            [0, BG_PLOT],
            [0.3, NEON_PURPLE],
            [0.65, NEON_CYAN],
            [1.0, NEON_LIME],
        ]
    elif hm_m == "Median Price":
        ca["value"] = ca["med"]
        vl, vs, fmt = "value", "Median £", ",.0f"
        cs = [
            [0, BG_PLOT],
            [0.3, NEON_PURPLE],
            [0.65, NEON_CYAN],
            [1.0, NEON_PINK],
        ]
    else:
        ca["value"] = ca["avg"]
        vl, vs, fmt = "value", "Avg £", ",.0f"
        cs = [
            [0, BG_PLOT],
            [0.3, NEON_PURPLE],
            [0.65, NEON_CYAN],
            [1.0, NEON_PINK],
        ]

    ca = ca.dropna(subset=[vl]).sort_values(vl, ascending=True)

    with hc2:
        f_hm = go.Figure(
            go.Bar(
                x=ca[vl],
                y=ca["county"].str[:22],
                orientation="h",
                marker=dict(
                    color=ca[vl],
                    colorscale=cs,
                    showscale=True,
                    colorbar=dict(
                        thickness=10,
                        tickfont=dict(size=8, color=TEXT_MUTED),
                        outlinewidth=0,
                        title=dict(text=vs, font=dict(size=8, color=TEXT_MUTED)),
                    ),
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{y}</b><br>" + vs + ": %{x:,.2f}<extra></extra>",
            )
        )
        theme(
            f_hm,
            f"UK COUNTY RANKINGS — {hm_m} ({hm_y})",
            h=max(450, len(ca) * 20),
        )
        f_hm.update_layout(margin=dict(l=10, r=60, t=100, b=10))
        f_hm.update_xaxes(
            tickprefix="£" if "Price" in hm_m else "",
            tickformat=",",
        )
        st.plotly_chart(f_hm, use_container_width=True)

    st.markdown("---")
    st.markdown(
        f'<div style="font-family:Orbitron;font-size:.65rem;color:{NEON_ORANGE};font-weight:900;margin-bottom:.5rem;text-shadow: 0 0 10px rgba(255, 102, 0, 0.4)">🗺️ YEAR-ON-YEAR PERFORMANCE BY COUNTY</div>',
        unsafe_allow_html=True,
    )

    # YoY by county heatmap
    yoy_y = st.selectbox(
        "Select year for YoY comparison",
        sorted(dff["year"].unique(), reverse=True),
        key="zone2_yoy_year",
        help="Shows price change from previous year for each county"
    )
    
    if yoy_y > dff["year"].min():
        # Calculate YoY for each county
        cur_year_prices = dff[dff["year"] == yoy_y].groupby("county")["price_paid"].mean()
        prev_year_prices = dff[dff["year"] == yoy_y-1].groupby("county")["price_paid"].mean()
        
        yoy_data = ((cur_year_prices - prev_year_prices) / prev_year_prices * 100).dropna()
        yoy_data = yoy_data.sort_values(ascending=False).reset_index()
        yoy_data.columns = ["County", "YoY Change %"]
        
        # Create color-coded bar chart (green for gains, red for losses)
        colors = [NEON_LIME if x >= 0 else NEON_PINK for x in yoy_data["YoY Change %"]]
        
        f_yoy = go.Figure(
            go.Bar(
                x=yoy_data["YoY Change %"],
                y=yoy_data["County"].str[:22],
                orientation="h",
                marker=dict(color=colors, opacity=0.85, line=dict(width=0)),
                text=[f"{v:+.1f}%" for v in yoy_data["YoY Change %"]],
                textposition="outside",
                textfont=dict(size=9, color=TEXT_COLOR),
                hovertemplate="<b>%{y}</b><br>YoY: %{x:+.1f}%<extra></extra>",
            )
        )
        
        f_yoy.add_vline(
            x=0,
            line_dash="dash",
            line_color=TEXT_MUTED,
            line_width=1.5
        )
        
        theme(
            f_yoy,
            tt(
                "YoY BY COUNTY",
                f"Year-on-year price changes from {yoy_y-1} to {yoy_y}. Green = price appreciation. Red = price decline."
            ),
            h=max(400, len(yoy_data) * 18),
        )
        f_yoy.update_layout(margin=dict(l=10, r=70, t=100, b=10))
        f_yoy.update_xaxes(ticksuffix="%")
        st.plotly_chart(f_yoy, use_container_width=True)
        
        cap(
            f"County performance visualized: Green bars show appreciation, red bars show decline. "
            f"Wider gaps indicate stronger YoY trends. Use this to identify emerging hotspots and cooling markets."
        )
    else:
        st.info("Select a year after the first year to see YoY comparisons.")

    st.markdown("---")
    st.markdown(
        f'<div style="font-family:Orbitron;font-size:.65rem;color:{NEON_TEAL};font-weight:900;margin-bottom:.5rem;text-shadow: 0 0 10px rgba(0, 255, 200, 0.4)">🔮 2026 PRICE PREDICTIONS</div>',
        unsafe_allow_html=True,
    )

    # Get ALL unique counties from the full unfiltered dataframe
    all_counties_list = sorted([str(c).upper().strip() for c in df["county"].dropna().unique() if c and str(c).upper().strip() != "NONE" and str(c).upper().strip() != ""])
    
    st.write(f"**Available counties: {len(all_counties_list)}**")
    
    pred_county = st.selectbox(
        "🎯 Select county for 2026 forecast",
        all_counties_list,
        key="zone2_pred_county_select",
    )

    pred = predict_2026_price(dff, pred_county)

    if pred["prediction"] is not None:
        # Calculate investment recommendation
        growth_pct = pred['growth']
        confidence_level = pred['confidence']
        
        # Buy/Hold/Sell logic:
        # HIGH growth + HIGH confidence = BUY (strong opportunity)
        # MEDIUM growth + MEDIUM+ confidence = HOLD (stable, monitor)
        # NEGATIVE growth + ANY confidence = SELL (declining market)
        if growth_pct >= 5 and confidence_level == "High":
            recommendation = "🟢 BUY"
            rec_color = NEON_LIME
            rec_reason = "Strong growth expected + high data quality = attractive investment"
        elif growth_pct >= 2 and confidence_level in ["High", "Medium"]:
            recommendation = "🟡 HOLD"
            rec_color = NEON_ORANGE
            rec_reason = "Modest growth + decent confidence = wait for better clarity"
        elif growth_pct < 0:
            recommendation = "🔴 SELL"
            rec_color = NEON_PINK
            rec_reason = "Decline expected = market cooling, avoid new purchases"
        elif growth_pct < 2:
            recommendation = "🟡 HOLD"
            rec_color = NEON_ORANGE
            rec_reason = "Minimal growth + uncertain forecast = insufficient opportunity"
        else:
            recommendation = "🟡 HOLD"
            rec_color = NEON_ORANGE
            rec_reason = "Mixed signals = wait for clearer direction"
        
        col_pred1, col_pred2, col_pred3, col_pred4, col_rec = st.columns([1, 1, 1, 1, 1.2])
        with col_pred1:
            st.metric(
                "2026 Predicted Price",
                f"£{pred['prediction']:,.0f}",
                delta=f"{pred['growth']:+.1f}%",
                help="ML forecast using polynomial regression on historical data.",
            )
        with col_pred2:
            st.metric(
                "Growth vs Now",
                f"{pred['growth']:+.1f}%",
                help="Expected price change from now to 2026.",
            )
        with col_pred3:
            st.metric(
                "Confidence",
                pred["confidence"],
                help=f"Based on data quality (MAPE: {pred['mape']:.1f}%). High = <5% error rate.",
            )
        with col_pred4:
            st.metric(
                "Data Points",
                pred["data"],
                help="Number of years used. Higher = more reliable.",
            )
        with col_rec:
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, rgba({rec_color[1:]}, 0.15), rgba({rec_color[1:]}, 0.05));
                    border: 2px solid {rec_color};
                    border-radius: 8px;
                    padding: 1.2rem;
                    text-align: center;
                    box-shadow: 0 0 25px rgba({rec_color[1:]}, 0.25);
                    font-family: 'Orbitron', sans-serif;
                ">
                    <div style="font-size: 2.5rem; margin-bottom: 0.8rem; letter-spacing: 0.1em">{recommendation}</div>
                    <div style="font-size: 0.8rem; color: {TEXT_MUTED}; line-height: 1.5; font-family: 'Space Grotesk', sans-serif">{rec_reason}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Visualization of prediction
        county_yearly = (
            dff[dff["county"] == pred_county]
            .groupby("year")["price_paid"]
            .mean()
            .reset_index()
        )
        county_yearly = county_yearly.sort_values("year")

        if len(county_yearly) > 0:
            X = county_yearly["year"].values
            y = county_yearly["price_paid"].values
            model = np.polyfit(X, y, 2)
            poly = np.poly1d(model)

            # Generate predictions for visualization
            future_years = np.array(
                list(range(int(X.min()), int(X.max()) + 1)) + [2026]
            )
            predictions = poly(future_years)

            f_pred = go.Figure()
            f_pred.add_trace(
                go.Scatter(
                    x=X,
                    y=y,
                    mode="markers",
                    name="Historical Data",
                    marker=dict(size=10, color=NEON_CYAN, opacity=0.8),
                    hovertemplate="Year: %{x}<br>Price: £%{y:,.0f}<extra></extra>",
                )
            )
            f_pred.add_trace(
                go.Scatter(
                    x=future_years,
                    y=predictions,
                    mode="lines",
                    name="Trend Forecast",
                    line=dict(color=NEON_PINK, width=3, dash="dash"),
                    hovertemplate="Year: %{x}<br>Predicted: £%{y:,.0f}<extra></extra>",
                )
            )
            f_pred.add_vline(
                x=2026,
                line_dash="dot",
                line_color=NEON_LIME,
                annotation_text="  2026",
                annotation_position="top right",
            )

            theme(
                f_pred,
                f"PRICE FORECAST — {pred_county} (Polynomial Regression)",
                h=320,
            )
            f_pred.update_yaxes(tickprefix="£", tickformat=",")
            st.plotly_chart(f_pred, use_container_width=True)

            cap(
                f"Cyan dots = historical averages. Pink dashed = polynomial trend extrapolated to 2026. "
                f"Method: degree-2 polynomial fit. "
                f"Accuracy depends on data consistency. High confidence ({pred['confidence']}) = more reliable prediction."
            )
        
        # Explain the recommendation logic using Streamlit containers
        st.divider()
        
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            with st.container(border=True):
                st.markdown(f"### 🟢 BUY", unsafe_allow_html=False)
                st.markdown(
                    f"**Growth ≥5% + High Confidence**  \n\n"
                    f"Strong opportunity with reliable data. Enter with confidence.",
                    unsafe_allow_html=False
                )
        
        with col_exp2:
            with st.container(border=True):
                st.markdown(f"### 🟡 HOLD", unsafe_allow_html=False)
                st.markdown(
                    f"**Growth 2-5% OR Growth <2%**  \n\n"
                    f"Positive but wait for clarity. Monitor before committing.",
                    unsafe_allow_html=False
                )
        
        with col_exp3:
            with st.container(border=True):
                st.markdown(f"### 🔴 SELL", unsafe_allow_html=False)
                st.markdown(
                    f"**Growth <0%**  \n\n"
                    f"Prices declining. Avoid new purchases. Consider exit.",
                    unsafe_allow_html=False
                )
        
        st.divider()
        
        # Confidence explanation
        st.markdown(
            f"**📊 Confidence Levels:** "
            f"High (excellent, <5% error) | "
            f"Medium (good, <10% error) | "
            f"Low (use caution, >10% error)",
            unsafe_allow_html=False
        )
    else:
        st.warning(f"Insufficient data for {pred_county} to make a 2026 forecast.")

# ══════════════════════════════════════════════════════════════════════════════
# ZONE 3 — GROWTH ENGINE
# ══════════════════════════════════════════════════════════════════════════════

with z3:
    zbanner("📈 Growth Engine — Historical performance & investment opportunities")

    cg_s = dff[dff["year"] == yr_start].groupby("county")["price_paid"].mean()
    cg_e = dff[dff["year"] == yr_end].groupby("county")["price_paid"].mean()
    cg = ((cg_e / cg_s) ** (1 / n_yrs) - 1).dropna().reset_index()
    cg.columns = ["county", "cagr"]
    cg = cg.sort_values("cagr", ascending=True)
    ag = cg["cagr"].mean()
    cg["col"] = cg["cagr"].apply(lambda x: NEON_LIME if x >= ag else NEON_PINK)

    f10 = go.Figure(
        go.Bar(
            x=cg["cagr"] * 100,
            y=cg["county"].str[:22],
            orientation="h",
            marker=dict(color=cg["col"], opacity=0.85, line=dict(width=0)),
            text=[f"{v*100:.1f}%" for v in cg["cagr"]],
            textposition="outside",
            textfont=dict(size=8, color=TEXT_COLOR),
            hovertemplate="<b>%{y}</b><br>CAGR: %{x:.2f}%<extra></extra>",
        )
    )
    f10.add_vline(
        x=ag * 100,
        line_dash="dash",
        line_color=NEON_CYAN,
        line_width=2,
        annotation_text=f" Avg {ag*100:.1f}%",
        annotation_font=dict(color=NEON_CYAN, size=9),
        annotation_position="top right",
    )
    theme(
        f10,
        tt(
            "CAGR BY COUNTY",
            "Compound Annual Growth Rate. A 5% CAGR = prices roughly double every 14 years. Green = above avg.",
        ),
        h=max(400, len(cg) * 20),
    )
    f10.update_layout(margin=dict(l=10, r=70, t=100, b=10))
    f10.update_xaxes(ticksuffix="%")
    st.plotly_chart(f10, use_container_width=True)
    cap("Green bars = counties growing faster than average. Red = lagging. Gold line = national average CAGR.")

    st.markdown("---")

    g3a, g3b = st.columns(2)

    with g3a:
        ptr = dff.groupby(["year", "Property Type"])["price_paid"].mean().reset_index()
        f12 = go.Figure()
        for i, pt in enumerate(["Detached", "Semi-Detached", "Terraced", "Flat", "Other"]):
            s = ptr[ptr["Property Type"] == pt]
            f12.add_trace(
                go.Scatter(
                    x=s["year"],
                    y=s["price_paid"],
                    name=pt,
                    mode="lines+markers",
                    line=dict(color=NEON_PALETTE[i % len(NEON_PALETTE)], width=2.5),
                    marker=dict(
                        size=6,
                        color=NEON_PALETTE[i % len(NEON_PALETTE)],
                        line=dict(color=BG_PLOT, width=1.5),
                    ),
                    hovertemplate=f"<b>{pt}</b><br>Year: %{{x}}<br>Avg: £%{{y:,.0f}}<extra></extra>",
                )
            )
        theme(
            f12,
            f"PRICE TRENDS BY {tt('PROPERTY TYPE', 'Detached = standalone. Semi = joined one side. Terraced = joined both. Flat = apartment. Each has different growth profile.')}",
            h=360,
        )
        f12.update_yaxes(tickprefix="£", tickformat=",")
        st.plotly_chart(f12, use_container_width=True)
        cap(
            "Detached commands highest prices and premium growth. Flats growing faster in cities = urbanisation trend. "
            "Diverging lines = market bifurcation by property type."
        )

    with g3b:
        nbt = dff.groupby(["year", "Build Type"])["price_paid"].mean().reset_index()
        f17 = go.Figure()
        for i, bt in enumerate(["New Build", "Existing"]):
            s = nbt[nbt["Build Type"] == bt]
            f17.add_trace(
                go.Scatter(
                    x=s["year"],
                    y=s["price_paid"],
                    name=bt,
                    mode="lines+markers",
                    line=dict(color=[NEON_LIME, NEON_CYAN][i], width=2.5),
                    marker=dict(
                        size=6,
                        color=[NEON_LIME, NEON_CYAN][i],
                        line=dict(color=BG_PLOT, width=1.5),
                    ),
                    hovertemplate=f"<b>{bt}</b><br>Year: %{{x}}<br>Avg: £%{{y:,.0f}}<extra></extra>",
                )
            )
        theme(
            f17,
            tt(
                "NEW BUILD PREMIUM",
                "Gap between lines = extra price for brand-new vs existing. Developers have pricing power.",
            ),
            h=360,
        )
        f17.update_yaxes(tickprefix="£", tickformat=",")
        st.plotly_chart(f17, use_container_width=True)
        cap(
            "Widening gap = developers have pricing power & buyers value new spec. "
            "Narrowing = premium eroding (scheme end, market saturation)."
        )


# ══════════════════════════════════════════════════════════════════════════════
# ZONE 4 — DEEP ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

with z4:
    zbanner("🔬 Deep Analysis — Distribution, volatility & micro-market dynamics")

    a1, a2 = st.columns(2)

    with a1:
        dy2 = st.selectbox(
            "Year",
            sorted(dff["year"].unique(), reverse=True),
            key="zone4_year_select_a",
        )
        dp2 = st.selectbox(
            "Property Type",
            ["All"] + sorted(dff["Property Type"].unique()),
            key="zone4_proptype_select",
        )
        sdi = dff[dff["year"] == dy2] if dp2 == "All" else dff[(dff["year"] == dy2) & (dff["Property Type"] == dp2)]
        sdi = sdi[sdi["price_paid"] < 2_000_000]
        av = sdi["price_paid"].mean()
        mv = sdi["price_paid"].median()
        f15 = go.Figure()
        f15.add_trace(
            go.Histogram(
                x=sdi["price_paid"],
                nbinsx=80,
                marker=dict(color=NEON_ORANGE, opacity=0.72, line=dict(width=0)),
                name="Transactions",
                hovertemplate="Price: £%{x:,.0f}<br>Count: %{y:,}<extra></extra>",
            )
        )
        f15.add_vline(
            x=av,
            line_color=NEON_CYAN,
            line_dash="dash",
            annotation_text=f"Mean: £{av:,.0f}",
            annotation_font=dict(color=NEON_CYAN, size=9, family="IBM Plex Mono"),
            annotation_position="top right",
        )
        f15.add_vline(
            x=mv,
            line_color=NEON_LIME,
            line_dash="dash",
            annotation_text=f"Median: £{mv:,.0f}",
            annotation_font=dict(color=NEON_LIME, size=9, family="IBM Plex Mono"),
            annotation_position="top left",
        )
        theme(
            f15,
            tt(
                "PRICE DISTRIBUTION",
                "Histogram of all sales. Narrow peak = uniform pricing. Long right tail = luxury outliers.",
            ),
            h=360,
        )
        f15.update_xaxes(tickprefix="£", tickformat=",")
        st.plotly_chart(f15, use_container_width=True)
        cap(
            "Cyan line (mean) pulled up by outliers. Green line (median) is what a typical buyer actually pays. "
            "Long tail right = ultra-luxury pulling average. For typical buyer: focus on median."
        )

    with a2:
        ay = st.selectbox(
            "Year",
            sorted(dff["year"].unique(), reverse=True),
            key="zone4_year_select_b",
        )
        sa = (
            dff[dff["year"] == ay]
            .groupby("county")
            .agg(avg=("price_paid", "mean"), cnt=("price_paid", "size"))
            .reset_index()
        )
        sa = sa[sa["cnt"] > 15]
        f16 = go.Figure(
            go.Scatter(
                x=sa["avg"],
                y=sa["cnt"],
                mode="markers",
                marker=dict(
                    size=(sa["cnt"].clip(upper=8000) / 300 + 8).clip(8, 32),
                    color=sa["avg"],
                    colorscale=[
                        [0, NEON_LIME],
                        [0.5, NEON_ORANGE],
                        [1.0, NEON_PINK],
                    ],
                    showscale=True,
                    opacity=0.8,
                    colorbar=dict(
                        thickness=8,
                        tickprefix="£",
                        tickformat=",",
                        tickfont=dict(size=8, color=TEXT_MUTED),
                        outlinewidth=0,
                    ),
                    line=dict(color=BG_PLOT, width=1),
                ),
                text=sa["county"].str[:18],
                hovertemplate="<b>%{text}</b><br>Avg: £%{x:,.0f}<br>Sales: %{y:,}<extra></extra>",
            )
        )
        theme(
            f16,
            tt(
                "AFFORDABILITY SCATTER",
                "X = price. Y = sales count (market liquidity). Bottom-right = best entry. Bubble size = market volume.",
            ),
            h=360,
        )
        f16.update_xaxes(tickprefix="£", tickformat=",")
        f16.update_yaxes(title_text="Sales Count")
        st.plotly_chart(f16, use_container_width=True)
        
        # Clear affordability explanation with quadrant breakdown
        st.divider()
        
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            with st.container(border=True):
                st.markdown("### 🟢 BOTTOM-LEFT\n**Affordable + Emerging**\nLow price, low volume = Good for budget buyers")
            with st.container(border=True):
                st.markdown("### 🔴 TOP-LEFT\n**Expensive + Illiquid**\nHigh price, low volume = AVOID (hard to sell)")
        
        with col_q2:
            with st.container(border=True):
                st.markdown("### 🟠 BOTTOM-RIGHT ✅\n**Affordable + Liquid**\nLow price, high volume = BEST for buyers")
            with st.container(border=True):
                st.markdown("### 🔴 TOP-RIGHT\n**Expensive + Active**\nHigh price, high volume = London effect")
        
        st.divider()
        st.markdown(
            "**X-axis:** Average price (left = cheaper) | "
            "**Y-axis:** Sales count (bottom = fewer) | "
            "**Bubble size:** Market concentration",
            unsafe_allow_html=False
        )

    st.markdown("---")

    b1, b2 = st.columns(2)

    with b1:
        etr = dff.groupby(["year", "Estate Type"]).size().reset_index(name="n")
        etot = etr.groupby("year")["n"].transform("sum")
        etr["pct"] = etr["n"] / etot * 100
        f20 = go.Figure()
        for i, et in enumerate(["Freehold", "Leasehold", "Unknown"]):
            s = etr[etr["Estate Type"] == et]
            if len(s):
                f20.add_trace(
                    go.Scatter(
                        x=s["year"],
                        y=s["pct"],
                        name=et,
                        mode="lines",
                        stackgroup="one",
                        line=dict(width=0.5, color=NEON_PALETTE[i]),
                        hovertemplate=f"<b>{et}</b><br>Year: %{{x}}<br>Share: %{{y:.1f}}%<extra></extra>",
                    )
                )
        theme(
            f20,
            tt(
                "ESTATE TYPE MIX",
                "Freehold = own land forever. Leasehold = own for fixed term, subject to ground rent. Rising leasehold = more flats.",
            ),
            h=320,
        )
        f20.update_yaxes(title_text="Market Share (%)")
        st.plotly_chart(f20, use_container_width=True)
        cap(
            "Rising leasehold share = urbanisation (more flats, less houses). "
            "Leasehold reform could shift dynamics — government intervening on ground rent."
        )

    with b2:
        tl1, tl2, tl3 = st.columns([1, 1, 2])
        with tl1:
            rb = st.selectbox(
                "Rank By",
                ["Avg Price", "Sales Volume", "Median Price"],
                key="zone4_rankby_select",
            )
        with tl2:
            nt = st.slider("Top N Towns", 10, 40, 20, key="zone4_topn_slider")
        with tl3:
            tc2 = st.selectbox(
                "Filter by County",
                ["All"] + sorted(dff["county"].dropna().unique()),
                key="zone4_county_select",
            )

        stw = dff if tc2 == "All" else dff[dff["county"] == tc2]
        ta = (
            stw.groupby("town")
            .agg(
                avg=("price_paid", "mean"),
                med=("price_paid", "median"),
                cnt=("price_paid", "size"),
            )
            .reset_index()
            .dropna()
        )
        sc2 = {"Avg Price": "avg", "Sales Volume": "cnt", "Median Price": "med"}[rb]
        ta = ta.sort_values(sc2, ascending=False).head(nt)
        f19 = go.Figure(
            go.Bar(
                x=ta[sc2],
                y=ta["town"].str[:22],
                orientation="h",
                marker=dict(
                    color=ta[sc2],
                    colorscale=(
                        [
                            [0, NEON_LIME],
                            [0.5, NEON_ORANGE],
                            [1.0, NEON_PINK],
                        ]
                        if rb != "Sales Volume"
                        else [
                            [0, BG_PLOT],
                            [0.5, NEON_CYAN],
                            [1.0, NEON_LIME],
                        ]
                    ),
                    showscale=False,
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{y}</b><br>Value: %{x:,.0f}<extra></extra>",
            )
        )
        theme(
            f19,
            f"TOP {nt} TOWNS — Ranked by {rb}",
            h=max(320, nt * 20),
        )
        f19.update_layout(margin=dict(l=10, r=10, t=100, b=10))
        f19.update_xaxes(
            tickprefix="£" if rb != "Sales Volume" else "",
            tickformat=",",
        )
        st.plotly_chart(f19, use_container_width=True)
        cap(f"Your town leaderboard ranked by {rb}. Use to spot premium towns, identify liquid markets, or find emerging opportunities.")

st.markdown("---")
st.markdown(
    f"""
<div style='font-family:"IBM Plex Mono",monospace;font-size:.55rem;color:{TEXT_MUTED};
     text-align:center;padding:1rem;border-top:1px solid {AXIS_COLOR};margin-top:1.5rem'>
  UK PROPERTY INTELLIGENCE TERMINAL · GOLDMAN SACHS ASSET MANAGEMENT ·<br>
  DATA: HM LAND REGISTRY PRICE PAID · ENGLAND & WALES ·<br>
  FOR ANALYTICAL PURPOSES ONLY · NOT INVESTMENT ADVICE
</div>""",
    unsafe_allow_html=True,
)
