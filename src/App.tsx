import { useState, useRef } from "react";
import logoImg from "@/imports/mountains.png";

/* ─── Palette ──────────────────────────────────────────────── */
const P = {
  bg: "#0B0F1A",
  surface: "#0E1521",
  surfaceHigh: "#111D2E",
  border: "#1B2A42",
  borderFocus: "#2563EB",
  blue: "#2563EB",
  blueLight: "#4A9EFF",
  blueTint: "rgba(37,99,235,0.12)",
  blueTintHover: "rgba(37,99,235,0.18)",
  text: "#E2E8F5",
  textSub: "#94A3B8",
  textMuted: "#4A5568",
  textDisabled: "#2D3A50",
  chipBg: "#131D2E",
  chipBorder: "#1E3050",
};

/* ─── Icons (inline SVG, 16 × 16 unless noted) ─────────────── */
function IconHome() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <path d="M2.25 7.5L9 2.25L15.75 7.5V15.75C15.75 16.1642 15.4142 16.5 15 16.5H3C2.58579 16.5 2.25 16.1642 2.25 15.75V7.5Z" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M6.75 16.5V10.5H11.25V16.5" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconHistory() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="6.75" stroke="currentColor" strokeWidth="1.25" />
      <path d="M9 5.25V9L11.25 11.25" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconSettings() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <circle cx="9" cy="9" r="2.25" stroke="currentColor" strokeWidth="1.25" />
      <path d="M9 1.5V3M9 15V16.5M1.5 9H3M15 9H16.5M3.698 3.698L4.76 4.76M13.24 13.24L14.302 14.302M14.302 3.698L13.24 4.76M4.76 13.24L3.698 14.302" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
    </svg>
  );
}

function IconPlus() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
      <path d="M9 3.75V14.25M3.75 9H14.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

function IconUpload({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path d="M4 16v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M16 8l-4-4-4 4M12 4v12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconLink({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconFigma({ size = 24 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      <rect x="5" y="2" width="14" height="7" rx="3.5" stroke="currentColor" strokeWidth="1.5" />
      <rect x="5" y="9" width="7" height="7" rx="3.5" stroke="currentColor" strokeWidth="1.5" />
      <circle cx="15.5" cy="12.5" r="3.5" stroke="currentColor" strokeWidth="1.5" />
      <rect x="5" y="16" width="7" height="7" rx="3.5" stroke="currentColor" strokeWidth="1.5" />
    </svg>
  );
}

function IconCheck({ size = 14 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 14 14" fill="none">
      <path d="M2.5 7L5.5 10L11.5 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconHelp() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="6.5" stroke="currentColor" strokeWidth="1.2" />
      <path d="M6.5 6.25C6.5 5.42157 7.17157 4.75 8 4.75C8.82843 4.75 9.5 5.42157 9.5 6.25C9.5 6.88 9.14 7.42 8.6 7.71C8.22 7.93 8 8.28 8 8.75V9.25" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
      <circle cx="8" cy="11" r="0.6" fill="currentColor" />
    </svg>
  );
}

function IconEye({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none">
      <path d="M1 8C1 8 3.27273 3 8 3C12.7273 3 15 8 15 8C15 8 12.7273 13 8 13C3.27273 13 1 8 1 8Z" stroke="currentColor" strokeWidth="1.2" />
      <circle cx="8" cy="8" r="2" stroke="currentColor" strokeWidth="1.2" />
    </svg>
  );
}

function IconLayers({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none">
      <path d="M1.5 8L8 11.5L14.5 8M1.5 11.5L8 15L14.5 11.5M8 1L1.5 4.5L8 8L14.5 4.5L8 1Z" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function IconTarget({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none">
      <circle cx="8" cy="8" r="6.5" stroke="currentColor" strokeWidth="1.2" />
      <circle cx="8" cy="8" r="3" stroke="currentColor" strokeWidth="1.2" />
      <circle cx="8" cy="8" r="1" fill="currentColor" />
    </svg>
  );
}

function IconSparkle({ size = 16 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 16 16" fill="none">
      <path d="M8 1.5L9.2 6L13.5 7L9.2 8L8 12.5L6.8 8L2.5 7L6.8 6L8 1.5Z" stroke="currentColor" strokeWidth="1.2" strokeLinejoin="round" />
    </svg>
  );
}

/* ─── Logo mark ─────────────────────────────────────────────── */
function LogoMark({ size = 28 }: { size?: number }) {
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: 8,
        overflow: "hidden",
        flexShrink: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <img
        src={logoImg}
        alt="UX Lens logo"
        style={{ width: "100%", height: "100%", objectFit: "contain" }}
      />
    </div>
  );
}

/* ─── Sidebar ───────────────────────────────────────────────── */
type NavItem = { icon: React.ReactNode; label: string; active?: boolean };

function Sidebar() {
  const items: NavItem[] = [
    {
      label: "Projects",
      icon: <svg width="17" height="17" viewBox="0 0 18 18" fill="none"><rect x="2.5" y="2.5" width="4" height="4" rx=".5" stroke="currentColor"/><rect x="11.5" y="2.5" width="4" height="4" rx=".5" stroke="currentColor"/><rect x="2.5" y="11.5" width="4" height="4" rx=".5" stroke="currentColor"/><rect x="11.5" y="11.5" width="4" height="4" rx=".5" stroke="currentColor"/></svg>,
    },
    {
      label: "Files",
      icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M2.25 5.25h5l1.5 1.5h7.5v6.75a1.5 1.5 0 0 1-1.5 1.5h-11.25A1.5 1.5 0 0 1 2 13.5V6.75a1.5 1.5 0 0 1 .25-1.5Z" stroke="currentColor" strokeWidth="1.25" strokeLinejoin="round"/></svg>,
    },
    {
      label: "New audit",
      active: true,
      icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><circle cx="9" cy="9" r="5.5" stroke="currentColor" strokeWidth="1.25"/><path d="M9 6v6M6 9h6" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round"/></svg>,
    },
    {
      label: "Reports",
      icon: <svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M5 2.75h6l2.5 2.5v10H5a1.5 1.5 0 0 1-1.5-1.5v-9.5A1.5 1.5 0 0 1 5 2.75Z" stroke="currentColor" strokeWidth="1.25"/><path d="M11 2.75v3h2.5" stroke="currentColor" strokeWidth="1.25"/></svg>,
    },
    { label: "Settings", icon: <IconSettings /> },
  ];

  return (
    <nav
      style={{
        width: 58,
        height: "100%",
        background: "#08294A",
        borderRight: "1px solid #12365B",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "14px 0",
        gap: 6,
        flexShrink: 0,
      }}
    >
      {items.map((item) => (
        <button
          key={item.label}
          type="button"
          title={item.label}
          aria-label={item.label}
          style={{
            width: 36,
            height: 36,
            border: "none",
            borderRadius: 9,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            background: item.active ? "#0E4D87" : "transparent",
            color: item.active ? "#55B7FF" : "#6E8EAD",
            transition: "background 0.15s, color 0.15s",
          }}
          onMouseEnter={(e) => {
            if (!item.active) {
              e.currentTarget.style.background = "rgba(255,255,255,0.06)";
              e.currentTarget.style.color = "#B5CCE0";
            }
          }}
          onMouseLeave={(e) => {
            if (!item.active) {
              e.currentTarget.style.background = "transparent";
              e.currentTarget.style.color = "#6E8EAD";
            }
          }}
        >
          {item.icon}
        </button>
      ))}
    </nav>
  );
}

/* ─── Top bar ───────────────────────────────────────────────── */
function TopBar() {
  return (
    <header
      style={{
        height: 52,
        background: P.surface,
        borderBottom: `1px solid ${P.border}`,
        display: "flex",
        alignItems: "center",
        padding: "0 24px 0 20px",
        flexShrink: 0,
        gap: 12,
      }}
    >
      {/* Logo + name */}
      <div style={{ display: "flex", alignItems: "center", gap: 9 }}>
        <LogoMark size={26} />
        <span
          style={{
            fontSize: 14,
            fontWeight: 800,
            color: P.text,
            letterSpacing: "0.4px",
          }}
        >
          UX LENS
        </span>
      </div>

      {/* Separator + breadcrumb */}
      <div style={{ width: 1, height: 18, background: P.border, marginLeft: 4 }} />
      <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
        <span style={{ fontSize: 12, color: P.textMuted, fontWeight: 500 }}>Projects</span>
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
          <path d="M4.5 9L7.5 6L4.5 3" stroke={P.textMuted} strokeOpacity={0.6} strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <span style={{ fontSize: 12, color: P.textSub, fontWeight: 500 }}>New audit</span>
      </div>

      <div style={{ flex: 1 }} />

      {/* Help button */}
      <button
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          background: "transparent",
          border: `1px solid ${P.border}`,
          borderRadius: 8,
          padding: "5px 11px",
          fontSize: 12,
          fontWeight: 500,
          color: P.textSub,
          cursor: "pointer",
          transition: "border-color 0.15s, color 0.15s",
        }}
        onMouseEnter={(e) => {
          (e.currentTarget as HTMLElement).style.borderColor = "rgba(74,158,255,0.35)";
          (e.currentTarget as HTMLElement).style.color = P.text;
        }}
        onMouseLeave={(e) => {
          (e.currentTarget as HTMLElement).style.borderColor = P.border;
          (e.currentTarget as HTMLElement).style.color = P.textSub;
        }}
      >
        <IconHelp />
        Help
      </button>

      {/* Avatar */}
      <div
        style={{
          width: 30,
          height: 30,
          borderRadius: "50%",
          background: "linear-gradient(135deg, #1d4ed8, #6d28d9)",
          border: `2px solid ${P.border}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 11,
          fontWeight: 700,
          color: "white",
          cursor: "pointer",
          letterSpacing: 0,
        }}
      >
        A
      </div>
    </header>
  );
}

/* ─── Source type tabs ──────────────────────────────────────── */
type SourceType = "upload" | "url" | "figma";

const TABS: { id: SourceType; label: string; icon: React.ReactNode }[] = [
  { id: "upload", label: "Upload screenshot", icon: <IconUpload size={16} /> },
  { id: "url", label: "Website URL", icon: <IconLink size={16} /> },
  { id: "figma", label: "Figma design", icon: <IconFigma size={16} /> },
];

/* ─── Audit focus chips ─────────────────────────────────────── */
const FOCUS_CHIPS = [
  "Visual hierarchy",
  "Accessibility",
  "Navigation",
  "Content clarity",
  "Conversion UX",
];

/* ─── Upload zone ───────────────────────────────────────────── */
function UploadZone({ onFile }: { onFile: (name: string) => void }) {
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      setFileName(file.name);
      onFile(file.name);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileName(file.name);
      onFile(file.name);
    }
  };

  return (
    <div style={{ padding: "4px 0 8px" }}>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        style={{
          border: `2px dashed ${dragging ? P.blueLight : fileName ? "rgba(37,99,235,0.5)" : P.border}`,
          borderRadius: 12,
          padding: "40px 24px",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
          cursor: "pointer",
          background: dragging ? P.blueTint : fileName ? "rgba(37,99,235,0.05)" : "transparent",
          transition: "all 0.2s",
        }}
      >
        <div
          style={{
            width: 48,
            height: 48,
            borderRadius: 12,
            background: dragging || fileName ? P.blueTint : P.chipBg,
            border: `1px solid ${dragging || fileName ? "rgba(37,99,235,0.3)" : P.chipBorder}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: dragging || fileName ? P.blueLight : P.textMuted,
            transition: "all 0.2s",
          }}
        >
          {fileName ? <IconCheck size={22} /> : <IconUpload size={22} />}
        </div>
        {fileName ? (
          <div style={{ textAlign: "center" }}>
            <p style={{ fontSize: 13, fontWeight: 500, color: P.blueLight, marginBottom: 2 }}>
              {fileName}
            </p>
            <p style={{ fontSize: 12, color: P.textMuted }}>Click to replace file</p>
          </div>
        ) : (
          <div style={{ textAlign: "center" }}>
            <p style={{ fontSize: 13, fontWeight: 500, color: P.textSub, marginBottom: 3 }}>
              Drop a PNG, JPG or WEBP here
            </p>
            <p style={{ fontSize: 12, color: P.textMuted }}>Maximum file size: 200 MB</p>
          </div>
        )}
        <button
          onClick={(e) => { e.stopPropagation(); inputRef.current?.click(); }}
          style={{
            marginTop: 4,
            background: "transparent",
            border: `1px solid ${P.border}`,
            borderRadius: 7,
            padding: "6px 16px",
            fontSize: 12,
            fontWeight: 500,
            color: P.textSub,
            cursor: "pointer",
            transition: "border-color 0.15s, color 0.15s",
          }}
          onMouseEnter={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = "rgba(74,158,255,0.4)";
            (e.currentTarget as HTMLElement).style.color = P.text;
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLElement).style.borderColor = P.border;
            (e.currentTarget as HTMLElement).style.color = P.textSub;
          }}
        >
          Browse files
        </button>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept=".png,.jpg,.jpeg,.webp"
        style={{ display: "none" }}
        onChange={handleChange}
      />
    </div>
  );
}

/* ─── URL Input ─────────────────────────────────────────────── */
function UrlInput({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  const [focused, setFocused] = useState(false);
  return (
    <div style={{ padding: "4px 0 8px" }}>
      <div
        style={{
          position: "relative",
          borderRadius: 10,
          border: `1px solid ${focused ? P.borderFocus : P.border}`,
          background: P.chipBg,
          transition: "border-color 0.15s",
          boxShadow: focused ? `0 0 0 3px rgba(37,99,235,0.15)` : "none",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: 14,
            top: "50%",
            transform: "translateY(-50%)",
            color: P.textMuted,
            pointerEvents: "none",
          }}
        >
          <IconLink size={16} />
        </div>
        <input
          type="url"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder="https://your-website.com"
          style={{
            width: "100%",
            background: "transparent",
            border: "none",
            outline: "none",
            padding: "13px 16px 13px 42px",
            fontSize: 14,
            color: P.text,
            fontFamily: "'Inter', sans-serif",
          }}
        />
      </div>
      <p style={{ marginTop: 8, fontSize: 12, color: P.textMuted, paddingLeft: 2 }}>
        We&apos;ll analyse the public page you provide.
      </p>
    </div>
  );
}

/* ─── Figma Input ───────────────────────────────────────────── */
function FigmaInput({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  const [focused, setFocused] = useState(false);
  return (
    <div style={{ padding: "4px 0 8px" }}>
      <div
        style={{
          position: "relative",
          borderRadius: 10,
          border: `1px solid ${focused ? P.borderFocus : P.border}`,
          background: P.chipBg,
          transition: "border-color 0.15s",
          boxShadow: focused ? `0 0 0 3px rgba(37,99,235,0.15)` : "none",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: 14,
            top: "50%",
            transform: "translateY(-50%)",
            color: P.textMuted,
            pointerEvents: "none",
          }}
        >
          <IconFigma size={16} />
        </div>
        <input
          type="url"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder="Paste a Figma file or frame link"
          style={{
            width: "100%",
            background: "transparent",
            border: "none",
            outline: "none",
            padding: "13px 16px 13px 42px",
            fontSize: 14,
            color: P.text,
            fontFamily: "'Inter', sans-serif",
          }}
        />
      </div>
      <p style={{ marginTop: 8, fontSize: 12, color: P.textMuted, paddingLeft: 2 }}>
        Analyse a frame, prototype, or design screen.
      </p>
    </div>
  );
}

/* ─── Main App ─────────────────────────────────────────────────*/
export default function App() {
  const [activeTab, setActiveTab] = useState<SourceType>("upload");
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [urlValue, setUrlValue] = useState("");
  const [figmaValue, setFigmaValue] = useState("");
  const [selectedFocus, setSelectedFocus] = useState<string[]>(["Visual hierarchy"]);

  const toggleFocus = (chip: string) => {
    setSelectedFocus((prev) =>
      prev.includes(chip) ? prev.filter((c) => c !== chip) : [...prev, chip]
    );
  };

  const isUrlValid = (url: string) => {
    try { new URL(url); return true; } catch { return false; }
  };

  const canStart =
    (activeTab === "upload" && uploadedFile !== null) ||
    (activeTab === "url" && isUrlValid(urlValue)) ||
    (activeTab === "figma" && figmaValue.trim().length > 0);

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: P.bg,
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
        color: P.text,
        overflow: "hidden",
      }}
    >
      <TopBar />

      <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
        <Sidebar />

        {/* ── Scrollable main content ── */}
        <main
          style={{
            flex: 1,
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            padding: "52px 24px 80px",
          }}
        >
          <div style={{ width: "100%", maxWidth: 640 }}>

            {/* ── Page heading ── */}
            <div style={{ textAlign: "center", marginBottom: 36 }}>
              <p
                style={{
                  fontSize: 11,
                  fontWeight: 700,
                  letterSpacing: "1.2px",
                  textTransform: "uppercase",
                  color: P.blueLight,
                  marginBottom: 10,
                }}
              >
                New Audit
              </p>
              <h1
                style={{
                  fontSize: 32,
                  fontWeight: 800,
                  color: P.text,
                  lineHeight: 1.2,
                  marginBottom: 12,
                  letterSpacing: "-0.5px",
                }}
              >
                Start a UX audit
              </h1>
              <p
                style={{
                  fontSize: 15,
                  color: P.textSub,
                  lineHeight: 1.65,
                  maxWidth: 480,
                  margin: "0 auto",
                }}
              >
                Add a website, screenshot, or design file to identify usability and visual hierarchy opportunities.
              </p>
            </div>

            {/* ── Source input card ── */}
            <div
              style={{
                background: P.surface,
                border: `1px solid ${P.border}`,
                borderRadius: 14,
                overflow: "hidden",
                marginBottom: 16,
                boxShadow: "0 4px 24px rgba(0,0,0,0.25)",
              }}
            >
              {/* Tab strip */}
              <div
                style={{
                  display: "flex",
                  borderBottom: `1px solid ${P.border}`,
                  background: P.bg,
                }}
              >
                {TABS.map((tab) => {
                  const active = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      style={{
                        flex: 1,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        gap: 7,
                        padding: "13px 12px",
                        background: active ? P.surface : "transparent",
                        border: "none",
                        borderBottom: active ? `2px solid ${P.blue}` : "2px solid transparent",
                        color: active ? P.text : P.textMuted,
                        fontSize: 13,
                        fontWeight: active ? 600 : 500,
                        cursor: "pointer",
                        transition: "all 0.15s",
                        fontFamily: "'Inter', sans-serif",
                        letterSpacing: "0.01em",
                        position: "relative",
                      }}
                      onMouseEnter={(e) => {
                        if (!active) (e.currentTarget as HTMLElement).style.color = P.textSub;
                      }}
                      onMouseLeave={(e) => {
                        if (!active) (e.currentTarget as HTMLElement).style.color = P.textMuted;
                      }}
                    >
                      <span style={{ opacity: active ? 1 : 0.6, color: active ? P.blueLight : "inherit" }}>
                        {tab.icon}
                      </span>
                      {tab.label}
                      {tab.id === "figma" && (
                        <span
                          style={{
                            background: "rgba(109,40,217,0.2)",
                            border: "1px solid rgba(109,40,217,0.35)",
                            borderRadius: 4,
                            padding: "1px 6px",
                            fontSize: 9,
                            fontWeight: 700,
                            color: "#a78bfa",
                            letterSpacing: "0.05em",
                          }}
                        >
                          BETA
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Tab content */}
              <div style={{ padding: "20px 24px 16px" }}>
                {activeTab === "upload" && (
                  <UploadZone onFile={(name) => setUploadedFile(name)} />
                )}
                {activeTab === "url" && (
                  <UrlInput value={urlValue} onChange={setUrlValue} />
                )}
                {activeTab === "figma" && (
                  <FigmaInput value={figmaValue} onChange={setFigmaValue} />
                )}
              </div>
            </div>

            {/* ── Audit focus ── */}
            <div
              style={{
                background: P.surface,
                border: `1px solid ${P.border}`,
                borderRadius: 14,
                padding: "20px 24px",
                marginBottom: 24,
                boxShadow: "0 4px 24px rgba(0,0,0,0.2)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: P.text }}>Audit focus</span>
                <span style={{ fontSize: 11, color: P.textMuted, fontWeight: 400 }}>
                  Select areas to prioritise
                </span>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 14 }}>
                {FOCUS_CHIPS.map((chip) => {
                  const selected = selectedFocus.includes(chip);
                  return (
                    <button
                      key={chip}
                      onClick={() => toggleFocus(chip)}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 6,
                        background: selected ? P.blueTint : P.chipBg,
                        border: `1px solid ${selected ? "rgba(37,99,235,0.45)" : P.chipBorder}`,
                        borderRadius: 20,
                        padding: "6px 14px",
                        fontSize: 12,
                        fontWeight: selected ? 600 : 500,
                        color: selected ? P.blueLight : P.textSub,
                        cursor: "pointer",
                        transition: "all 0.15s",
                        fontFamily: "'Inter', sans-serif",
                      }}
                      onMouseEnter={(e) => {
                        if (!selected) {
                          (e.currentTarget as HTMLElement).style.borderColor = "rgba(74,158,255,0.3)";
                          (e.currentTarget as HTMLElement).style.color = P.text;
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!selected) {
                          (e.currentTarget as HTMLElement).style.borderColor = P.chipBorder;
                          (e.currentTarget as HTMLElement).style.color = P.textSub;
                        }
                      }}
                    >
                      {selected && (
                        <span style={{ color: P.blue, display: "flex" }}>
                          <IconCheck size={12} />
                        </span>
                      )}
                      {chip}
                    </button>
                  );
                })}
              </div>
              <p style={{ fontSize: 11, color: P.textMuted, display: "flex", alignItems: "center", gap: 5 }}>
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                  <circle cx="6.5" cy="6.5" r="5.5" stroke={P.textMuted} strokeWidth="1" />
                  <path d="M6.5 5.5V9" stroke={P.textMuted} strokeWidth="1" strokeLinecap="round" />
                  <circle cx="6.5" cy="4" r="0.5" fill={P.textMuted} />
                </svg>
                You can refine the audit scope after adding your source.
              </p>
            </div>

            {/* ── CTA ── */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
              <button
                disabled={!canStart}
                style={{
                  width: "100%",
                  padding: "14px 24px",
                  borderRadius: 11,
                  background: canStart
                    ? "linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%)"
                    : P.chipBg,
                  border: `1px solid ${canStart ? "rgba(37,99,235,0.6)" : P.chipBorder}`,
                  color: canStart ? "#fff" : P.textDisabled,
                  fontSize: 15,
                  fontWeight: 700,
                  cursor: canStart ? "pointer" : "not-allowed",
                  letterSpacing: "0.01em",
                  transition: "all 0.2s",
                  fontFamily: "'Inter', sans-serif",
                  boxShadow: canStart ? "0 4px 20px rgba(37,99,235,0.35)" : "none",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 9,
                }}
                onMouseEnter={(e) => {
                  if (canStart) {
                    (e.currentTarget as HTMLElement).style.background =
                      "linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%)";
                    (e.currentTarget as HTMLElement).style.boxShadow =
                      "0 6px 28px rgba(37,99,235,0.45)";
                    (e.currentTarget as HTMLElement).style.transform = "translateY(-1px)";
                  }
                }}
                onMouseLeave={(e) => {
                  if (canStart) {
                    (e.currentTarget as HTMLElement).style.background =
                      "linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%)";
                    (e.currentTarget as HTMLElement).style.boxShadow =
                      "0 4px 20px rgba(37,99,235,0.35)";
                    (e.currentTarget as HTMLElement).style.transform = "none";
                  }
                }}
              >
                {canStart ? (
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M8 1.5L9.2 6L13.5 7L9.2 8L8 12.5L6.8 8L2.5 7L6.8 6L8 1.5Z" fill="white" />
                  </svg>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <rect x="4" y="7" width="8" height="6" rx="1" stroke={P.textDisabled} strokeWidth="1.2" />
                    <path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2" stroke={P.textDisabled} strokeWidth="1.2" strokeLinecap="round" />
                  </svg>
                )}
                Start UX Audit
              </button>
              <p style={{ fontSize: 12, color: P.textMuted }}>
                Your source is only used to generate this audit.
              </p>
            </div>

            {/* ── Benefits strip ── */}
            <div
              style={{
                display: "flex",
                gap: 0,
                marginTop: 48,
                borderTop: `1px solid ${P.border}`,
                paddingTop: 32,
              }}
            >
              {[
                { icon: <IconEye size={14} />, label: "Find usability friction", desc: "Identify friction points before users do." },
                { icon: <IconLayers size={14} />, label: "Improve visual clarity", desc: "Sharpen hierarchy, spacing, and contrast." },
                { icon: <IconSparkle size={14} />, label: "Get actionable recommendations", desc: "Prioritised fixes you can act on immediately." },
              ].map((b, i) => (
                <div
                  key={b.label}
                  style={{
                    flex: 1,
                    padding: "0 20px",
                    borderLeft: i > 0 ? `1px solid ${P.border}` : "none",
                    display: "flex",
                    flexDirection: "column",
                    gap: 6,
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
                    <div
                      style={{
                        width: 28,
                        height: 28,
                        borderRadius: 8,
                        background: P.chipBg,
                        border: `1px solid ${P.chipBorder}`,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: P.blueLight,
                        flexShrink: 0,
                      }}
                    >
                      {b.icon}
                    </div>
                    <span style={{ fontSize: 12, fontWeight: 600, color: P.text }}>{b.label}</span>
                  </div>
                  <p style={{ fontSize: 11, color: P.textMuted, lineHeight: 1.55, paddingLeft: 0 }}>
                    {b.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
