"""
UX Lens AI — Main Application
app.py

Streamlit interface for the UX Lens AI accessibility and
visual-clarity audit prototype.

Run:
    streamlit run app.py
"""
const { useState } = React;

const severityColor = (s) => ({ HIGH: "#EF4444", MEDIUM: "#F59E0B", LOW: "#22C55E" }[s] || "#38BDF8");

const findings = [
  { title: "Fix button contrast", description: "The View details button has a 2.6:1 contrast ratio. Increase to at least 4.5.", severity: "HIGH" },
  { title: "Improve secondary text readability", description: "Balance labels and account metadata are difficult to read on white backgrounds.", severity: "HIGH" },
  { title: "Increase touch target size", description: "The Payments action is 28×28px. WCAG recommends at least 44×44px.", severity: "MEDIUM" },
  { title: "Strengthen chart contrast", description: "Monthly spending bars blend into the chart background.", severity: "MEDIUM" },
  { title: "Navigation structure is clear", description: "Bottom navigation has a consistent icon layout.", severity: "LOW" },
];

const metrics = [
  { label: "ACCESSIBILITY", value: "62%", grade: "C", color: "#EF4444" },
  { label: "USABILITY", value: "88%", grade: "A", color: "#22C55E" },
  { label: "VISUAL CLARITY", value: "81%", grade: "B", color: "#F59E0B" },
  { label: "PERFORMANCE", value: "90%", grade: "A", color: "#22C55E" },
];

function DonutChart({ score }) {
  const r = 40, cx = 50, cy = 50;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;
  return (
    <svg viewBox="0 0 100 100" width="90" height="90">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1A3A5C" strokeWidth="10" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#F59E0B" strokeWidth="10"
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 50 50)" />
      <text x="50" y="46" textAnchor="middle" fill="#F5F9FF" fontSize="16" fontWeight="800">{score}%</text>
      <text x="50" y="60" textAnchor="middle" fill="#22C55E" fontSize="9" fontWeight="700">B</text>
    </svg>
  );
}

function App() {
  const [auditRun, setAuditRun] = useState(true);
  const [activeNav, setActiveNav] = useState("audit");

  const navIcons = [
    { id: "grid", icon: "⊞" },
    { id: "folder", icon: "⊟" },
    { id: "audit", icon: "◉" },
    { id: "report", icon: "≡" },
    { id: "settings", icon: "⚙" },
  ];

  return (
    <div style={{ display: "flex", height: "100vh", background: "#061426", color: "#E9F2FF", fontFamily: "Inter, sans-serif", fontSize: "13px" }}>

      {/* Left icon nav */}
      <div style={{ width: "44px", background: "#050F1E", borderRight: "1px solid #0F2540", display: "flex", flexDirection: "column", alignItems: "center", paddingTop: "12px", gap: "6px" }}>
        <div style={{ width: "28px", height: "28px", background: "#1A3A5C", borderRadius: "6px", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: "12px" }}>
          <span style={{ fontSize: "14px" }}>◎</span>
        </div>
        {navIcons.map(n => (
          <div key={n.id} onClick={() => setActiveNav(n.id)}
            style={{ width: "32px", height: "32px", borderRadius: "8px", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", fontSize: "16px",
              background: activeNav === n.id ? "#0D2A4A" : "transparent",
              color: activeNav === n.id ? "#268CFF" : "#4A6A8A" }}>
            {n.icon}
          </div>
        ))}
        <div style={{ marginTop: "auto", marginBottom: "12px" }}>
          <div style={{ width: "28px", height: "28px", borderRadius: "50%", background: "#268CFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "11px", fontWeight: "700" }}>C</div>
        </div>
      </div>

      {/* Main area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>

        {/* Top bar */}
        <div style={{ height: "44px", background: "#061426", borderBottom: "1px solid #0F2540", display: "flex", alignItems: "center", padding: "0 16px", gap: "8px" }}>
          <span style={{ color: "#F5F9FF", fontWeight: "800", fontSize: "14px" }}>UX LENS</span>
          <span style={{ color: "#4A6A8A" }}>›</span>
          <span style={{ color: "#4A6A8A" }}>Projects</span>
          <span style={{ color: "#4A6A8A" }}>›</span>
          <span style={{ color: "#4A6A8A" }}>NOVA ATELIER Page Web</span>
          <span style={{ color: "#4A6A8A" }}>›</span>
          <span style={{ color: "#E9F2FF" }}>Accessibility Audit</span>
          <div style={{ marginLeft: "auto", display: "flex", gap: "8px", alignItems: "center" }}>
            <div style={{ background: "#0D3320", border: "1px solid #22C55E", borderRadius: "6px", padding: "4px 10px", color: "#22C55E", fontSize: "11px", fontWeight: "700" }}>● Scan complete</div>
            <button style={{ background: "#0A203A", border: "1px solid #2A4B6D", borderRadius: "6px", padding: "4px 10px", color: "#E9F2FF", fontSize: "11px", cursor: "pointer" }}>↑ Export report</button>
            <button style={{ background: "#268CFF", border: "none", borderRadius: "6px", padding: "4px 12px", color: "#fff", fontSize: "11px", fontWeight: "700", cursor: "pointer" }}>Share</button>
          </div>
        </div>

        {/* Content row */}
        <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>

          {/* Center: preview */}
          <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
            {/* Sub-header */}
            <div style={{ padding: "10px 16px", borderBottom: "1px solid #0F2540", display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ fontWeight: "700", fontSize: "13px" }}>NOVA ATELIER — Homepage</span>
              <span style={{ background: "#0D2A4A", border: "1px solid #268CFF", borderRadius: "4px", padding: "2px 7px", color: "#268CFF", fontSize: "10px", fontWeight: "700" }}>LIVE AUDIT</span>
              <span style={{ background: "#0A203A", border: "1px solid #2A4B6D", borderRadius: "4px", padding: "2px 7px", color: "#7891AE", fontSize: "10px" }}>Page web</span>
              <span style={{ background: "#0A203A", border: "1px solid #2A4B6D", borderRadius: "4px", padding: "2px 7px", color: "#7891AE", fontSize: "10px" }}>WCAG 2.1 AA</span>
              <div style={{ marginLeft: "auto", display: "flex", gap: "8px" }}>
                <button style={{ background: "#0A203A", border: "1px solid #2A4B6D", borderRadius: "6px", padding: "4px 10px", color: "#E9F2FF", fontSize: "11px", cursor: "pointer" }}>⊡ Snap</button>
                <button style={{ background: "#268CFF", border: "none", borderRadius: "6px", padding: "4px 12px", color: "#fff", fontSize: "11px", fontWeight: "700", cursor: "pointer" }}>Search</button>
              </div>
            </div>

            {/* Preview area */}
            <div style={{ flex: 1, background: "#040D1A", display: "flex", alignItems: "center", justifyContent: "center", color: "#2A4B6D", fontSize: "13px" }}>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: "32px", marginBottom: "8px" }}>◎</div>
                <div>Upload a screenshot to preview the interface</div>
              </div>
            </div>
          </div>

          {/* Right panel: audit results */}
          <div style={{ width: "280px", background: "#071B32", borderLeft: "1px solid #0F2540", display: "flex", flexDirection: "column", overflow: "hidden" }}>
            <div style={{ padding: "14px 14px 0 14px" }}>
              <div style={{ color: "#7891AE", fontSize: "9px", fontWeight: "800", letterSpacing: "1px", marginBottom: "4px" }}>UX AUDIT RESULTS</div>
              <div style={{ color: "#F5F9FF", fontWeight: "800", fontSize: "14px", marginBottom: "12px" }}>Finova Mobile App</div>

              {/* Score donut */}
              <div style={{ background: "#0A203A", border: "1px solid #1A3A5C", borderRadius: "10px", padding: "12px", marginBottom: "10px", display: "flex", alignItems: "center", gap: "12px" }}>
                <DonutChart score={78} />
                <div>
                  <div style={{ color: "#F5F9FF", fontWeight: "800", fontSize: "16px" }}>Good foundation</div>
                  <div style={{ color: "#7891AE", fontSize: "10px", marginTop: "4px" }}>Accessibility needs attention</div>
                </div>
              </div>

              {/* Metrics grid */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px", marginBottom: "10px" }}>
                {metrics.map(m => (
                  <div key={m.label} style={{ background: "#0A203A", border: "1px solid #173451", borderRadius: "8px", padding: "8px 10px" }}>
                    <div style={{ color: "#7891AE", fontSize: "8px", fontWeight: "800", letterSpacing: "0.5px", marginBottom: "4px" }}>{m.label}</div>
                    <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
                      <span style={{ color: m.color, fontSize: "20px", fontWeight: "800" }}>{m.value}</span>
                      <span style={{ background: m.color, color: "#061426", borderRadius: "4px", padding: "1px 5px", fontSize: "9px", fontWeight: "800" }}>{m.grade}</span>
                    </div>
                    <div style={{ height: "2px", background: m.color, borderRadius: "2px", marginTop: "6px", opacity: 0.7 }} />
                  </div>
                ))}
              </div>

              {/* Findings header */}
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
                <span style={{ color: "#F5F9FF", fontWeight: "700", fontSize: "12px" }}>Actionable Insights</span>
                <span style={{ background: "#268CFF22", border: "1px solid #268CFF55", color: "#268CFF", borderRadius: "999px", padding: "1px 7px", fontSize: "9px", fontWeight: "800" }}>{findings.length} items</span>
              </div>
            </div>

            {/* Findings list */}
            <div style={{ flex: 1, overflowY: "auto", padding: "0 14px 14px 14px" }}>
              {findings.map((f, i) => {
                const color = severityColor(f.severity);
                return (
                  <div key={i} style={{ background: "#0A203A", border: "1px solid #173451", borderRadius: "8px", padding: "10px", marginBottom: "6px", cursor: "pointer" }}>
                    <div style={{ display: "flex", alignItems: "flex-start", gap: "8px" }}>
                      <span style={{ color, fontSize: "12px", marginTop: "1px" }}>◉</span>
                      <div style={{ flex: 1 }}>
                        <div style={{ color: "#E9F2FF", fontWeight: "700", fontSize: "11px", marginBottom: "3px" }}>{f.title}</div>
                        <div style={{ color: "#7891AE", fontSize: "10px", lineHeight: "1.4", marginBottom: "6px" }}>{f.description}</div>
                        <span style={{ background: color + "22", color, border: `1px solid ${color}55`, borderRadius: "999px", padding: "2px 7px", fontSize: "9px", fontWeight: "800" }}>{f.severity}</span>
                      </div>
                      <span style={{ color: "#4A6A8A", fontSize: "12px" }}>›</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Bottom actions */}
            <div style={{ padding: "10px 14px", borderTop: "1px solid #0F2540" }}>
              <div style={{ color: "#7891AE", fontSize: "9px", marginBottom: "8px" }}>⏱ Last scan: Today, 9:41 AM</div>
              <div style={{ display: "flex", gap: "6px" }}>
                <button style={{ flex: 1, background: "#0A203A", border: "1px solid #2A4B6D", borderRadius: "6px", padding: "7px", color: "#E9F2FF", fontSize: "10px", fontWeight: "700", cursor: "pointer" }}>View full report</button>
                <button style={{ flex: 1, background: "#268CFF", border: "none", borderRadius: "6px", padding: "7px", color: "#fff", fontSize: "10px", fontWeight: "700", cursor: "pointer" }}>Apply safe fixes</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
