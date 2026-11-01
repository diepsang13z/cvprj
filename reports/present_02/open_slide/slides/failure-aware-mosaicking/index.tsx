import type { DesignSystem, Page, SlideMeta } from '@open-slide/core';

/* ------------------------------------------------------------------ *
 * Design system: tông khảo sát bản đồ: nền drone-night, mực survey-amber
 * cho tín hiệu "cần chú ý", teal cho trạng thái đã kiểm chứng.
 * ------------------------------------------------------------------ */
export const design: DesignSystem = {
  palette: {
    bg: '#0b0f14',
    text: '#f2f5f8',
    accent: '#ff9f43',
  },
  fonts: {
    display: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
    body: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  },
  typeScale: { hero: 124, body: 32 },
  radius: 14,
};

const surface = '#121a22';
const line = '#1e2833';
const muted = '#8593a3';
const ok = '#4ecdc4';
const danger = '#ff5c5c';

const mono = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';

const fill = {
  width: '100%',
  height: '100%',
  fontFamily: 'var(--osd-font-body)',
} as const;

const page = {
  ...fill,
  background: 'var(--osd-bg)',
  color: 'var(--osd-text)',
  padding: '65px 96px',
  display: 'flex',
  flexDirection: 'column',
} as const;

/* ------------------------------------------------------------------ *
 * Khối dùng lại
 * ------------------------------------------------------------------ */

const Crumb = ({ n, label }: { n: string; label: string }) => (
  <div style={{ display: 'flex', alignItems: 'baseline', gap: 16 }}>
    <span
      style={{
        fontFamily: mono,
        fontSize: 22,
        fontWeight: 700,
        color: 'var(--osd-accent)',
        letterSpacing: '0.06em',
      }}
    >
      {n}
    </span>
    <span style={{ fontFamily: mono, fontSize: 20, color: muted, letterSpacing: '0.12em' }}>
      {label}
    </span>
  </div>
);

const Head = ({ n, label, title, sub }: { n: string; label: string; title: string; sub: string }) => (
  <div style={{ borderBottom: `1px solid ${line}`, paddingBottom: 16 }}>
    <Crumb n={n} label={label} />
    <h2
      style={{
        fontFamily: 'var(--osd-font-display)',
        fontSize: 56,
        fontWeight: 800,
        lineHeight: 1.15,
        letterSpacing: '-0.02em',
        margin: '12px 0 0',
      }}
    >
      {title}
    </h2>
    <p style={{ fontSize: 25, lineHeight: 1.45, color: muted, margin: '6px 0 0' }}>{sub}</p>
  </div>
);

const Panel = ({
  children,
  tone = 'plain',
}: {
  children: React.ReactNode;
  tone?: 'plain' | 'accent' | 'ok' | 'bad';
}) => {
  const edge = tone === 'accent' ? 'var(--osd-accent)' : tone === 'ok' ? ok : tone === 'bad' ? danger : line;
  return (
    <div
      style={{
        background: surface,
        border: `1px solid ${tone === 'plain' ? line : edge}`,
        borderTop: `3px solid ${edge}`,
        borderRadius: 'var(--osd-radius)',
        padding: '18px 24px',
        display: 'flex',
        flexDirection: 'column',
        gap: 10,
      }}
    >
      {children}
    </div>
  );
};

const titleStyle = {
  fontSize: 26,
  fontWeight: 700,
  lineHeight: 1.25,
  letterSpacing: '-0.01em',
} as const;

const bodyStyle = {
  fontSize: 23,
  lineHeight: 1.45,
  color: muted,
  margin: 0,
} as const;

const Th = ({ children, w }: { children: React.ReactNode; w?: number }) => (
  <th
    style={{
      width: w,
      textAlign: 'left',
      fontFamily: mono,
      fontSize: 20,
      fontWeight: 600,
      letterSpacing: '0.04em',
      color: muted,
      padding: '0 16px 10px',
      borderBottom: `2px solid ${line}`,
    }}
  >
    {children}
  </th>
);

const Td = ({ children, strong, tone }: { children: React.ReactNode; strong?: boolean; tone?: string }) => (
  <td
    style={{
      fontSize: 22,
      lineHeight: 1.35,
      padding: '9px 16px',
      borderBottom: `1px solid ${line}`,
      color: tone ?? (strong ? 'var(--osd-text)' : muted),
      fontWeight: strong ? 700 : 400,
    }}
  >
    {children}
  </td>
);

const Verdict = ({ tone, children }: { tone: 'ok' | 'accent' | 'bad'; children: React.ReactNode }) => (
  <span
    style={{
      fontFamily: mono,
      fontSize: 17,
      fontWeight: 700,
      padding: '3px 8px',
      borderRadius: 5,
      color: tone === 'ok' ? ok : tone === 'accent' ? 'var(--osd-accent)' : danger,
      background:
        tone === 'ok' ? 'rgba(78,205,196,0.12)' : tone === 'accent' ? 'rgba(255,159,67,0.12)' : 'rgba(255,92,92,0.12)',
    }}
  >
    {children}
  </span>
);

/* ------------------------------------------------------------------ *
 * 01: Cover
 * ------------------------------------------------------------------ */
const Cover: Page = () => (
  <div
    style={{
      ...fill,
      background: 'var(--osd-bg)',
      color: 'var(--osd-text)',
      padding: '0 150px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}
  >
    <div style={{ fontFamily: mono, fontSize: 24, color: 'var(--osd-accent)', letterSpacing: '0.14em' }}>
      BÁO CÁO TIẾN ĐỘ PRESENT 2 · HỌC PHẦN DAP391M
    </div>
    <h1
      style={{
        fontFamily: 'var(--osd-font-display)',
        fontSize: 92,
        fontWeight: 850,
        lineHeight: 1.15,
        letterSpacing: '-0.03em',
        margin: '24px 0 20px',
      }}
    >
      Failure-Aware & Resource-Adaptive
      <br />
      <span style={{ color: 'var(--osd-accent)' }}>2D Aerial Mosaicking from UAV Video</span>
    </h1>
    <div
      style={{
        fontSize: 27,
        color: 'var(--osd-text)',
        fontWeight: 500,
        marginBottom: 16,
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}
    >
      <span
        style={{
          color: ok,
          fontFamily: mono,
          fontSize: 18,
          fontWeight: 700,
          background: 'rgba(78,205,196,0.14)',
          padding: '3px 10px',
          borderRadius: 4,
          letterSpacing: '0.04em',
        }}
      >
        TẠM DỊCH
      </span>
      <span>Ghép ảnh 2D từ video UAV tự nhận biết lỗi và thích ứng tài nguyên</span>
    </div>
    <p style={{ fontSize: 28, lineHeight: 1.5, color: muted, maxWidth: 1250, margin: 0 }}>
      Làm sao dán hàng trăm bức ảnh rời rạc từ flycam thành 1 bản đồ lớn mà không bị méo,
      không làm đơ máy tính, và tự cứu vãn bản đồ khi bay qua địa hình hiểm trở?
    </p>
    <div style={{ display: 'flex', gap: 64, marginTop: 56 }}>
      <div>
        <div style={{ fontFamily: mono, fontSize: 21, color: muted, letterSpacing: '0.08em' }}>
          BÀI TOÁN
        </div>
        <div style={{ fontSize: 28, fontWeight: 650, marginTop: 6 }}>UAV 2D Aerial Mosaicking</div>
      </div>
      <div>
        <div style={{ fontFamily: mono, fontSize: 21, color: muted, letterSpacing: '0.08em' }}>
          DỮ LIỆU THẬT
        </div>
        <div style={{ fontSize: 28, fontWeight: 650, marginTop: 6 }}>NPU Drone-Map · Phantom 3</div>
      </div>
      <div>
        <div style={{ fontFamily: mono, fontSize: 21, color: muted, letterSpacing: '0.08em' }}>
          TIẾN ĐỘ
        </div>
        <div style={{ fontSize: 28, fontWeight: 650, marginTop: 6, color: ok }}>
          Đã chạy thực nghiệm & kiểm chứng 5 Notebook
        </div>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 02: Bài toán & 3 RQ
 * ------------------------------------------------------------------ */
const Problem: Page = () => (
  <div style={page}>
    <Head
      n="01"
      label="BÀI TOÁN & THÁCH THỨC"
      title="Dán ảnh flycam: Sai một ly, đi một dặm!"
      sub="Tưởng tượng bạn dán 45 tấm ảnh liên tiếp: Chỉ cần tấm thứ 5 bị lệch 2 độ, tấm 45 sẽ bị vặn rách toạc"
    />
    <div style={{ marginTop: 44, display: 'flex', flexDirection: 'column', gap: 30, flex: 1, minHeight: 0 }}>
      <Panel tone="accent">
        <div style={titleStyle}>Càng dán nhiều ảnh, sai số tích luỹ (Drift) càng khổng lồ</div>
        <p style={bodyStyle}>
          Máy tính dán ảnh tuần tự: Ảnh 2 dán vào Ảnh 1, Ảnh 3 dán vào Ảnh 2... Mỗi lần dán đều có một chút sai số nhỏ.
          Khi bay qua bãi cỏ trơn hoặc lúc drone quay đầu gắt, sai số này nhân dồn lên khiến cả tấm bản đồ bị xoắn vặn và biến dạng hoàn toàn.
        </p>
      </Panel>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26, flex: 1, minHeight: 0 }}>
        <Panel>
          <Crumb n="RQ1" label="BẮT BỆNH GHÉP SAI" />
          <div style={titleStyle}>Làm sao biết tấm ảnh vừa dán bị lệch?</div>
          <p style={bodyStyle}>
            Không có bản đồ vệ tinh chuẩn ngoài đời để so sánh. Nhóm phải tìm ra chỉ báo rẻ tiền giúp máy tính tự phát hiện bước dán hỏng ngay lập tức.
          </p>
        </Panel>
        <Panel>
          <Crumb n="RQ2" label="GỌI CỨU VIỆN" />
          <div style={titleStyle}>Khi nào dùng thuật toán nhẹ, khi nào gọi AI?</div>
          <p style={bodyStyle}>
            Bật AI cho mọi ảnh thì máy tính đơ cứng (chậm gấp 19 lần). Phân luồng thông minh: Bình thường chạy nhẹ, chỉ gọi AI xịn ở bước khó.
          </p>
        </Panel>
        <Panel>
          <Crumb n="RQ3" label="CỨU NGUY BẢN ĐỒ" />
          <div style={titleStyle}>Nếu AI cũng bó tay thì cứu bản đồ thế nào?</div>
          <p style={bodyStyle}>
            Gặp mặt cỏ mất vân hoàn toàn: Vứt ảnh thì mất video, cố dán thì rách bản đồ. Nhóm tìm ra cơ chế tự cứu tối ưu nhất để bảo toàn dữ liệu.
          </p>
        </Panel>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 03: Related works
 * ------------------------------------------------------------------ */
const RelatedWorks: Page = () => (
  <div style={page}>
    <Head
      n="02"
      label="NGHIÊN CỨU LIÊN QUAN"
      title="Hai thái cực: Cổ điển quá yếu: AI lại quá nặng"
      sub="Khảo sát 18 bài báo khoa học quốc tế để tìm ra lời giải dung hoà hoàn hảo"
    />
    <div style={{ marginTop: 44, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26, flex: 1, minHeight: 0 }}>
      <Panel>
        <div style={titleStyle}>1. Thuật toán Cổ điển (SIFT / ORB)</div>
        <p style={bodyStyle}>
          Dùng toán học thuần tuý để tìm góc cạnh (Hwang 2026, Li 2023).
        </p>
        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ fontSize: 25, color: ok }}>✓ Siêu nhanh, chạy mượt mà trên laptop</div>
          <div style={{ fontSize: 25, color: danger }}>✗ Mù quáng khi bay qua mặt cỏ, mặt nước</div>
          <div style={{ fontSize: 25, color: danger }}>✗ Không hề biết bản thân đang ghép sai</div>
        </div>
      </Panel>
      <Panel>
        <div style={titleStyle}>2. Trí tuệ nhân tạo (LightGlue, LoFTR)</div>
        <p style={bodyStyle}>
          Dùng mạng nơ-ron sâu Transformer để hiểu ngữ cảnh (Kim 2025).
        </p>
        <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 10 }}>
          <div style={{ fontSize: 25, color: ok }}>✓ Ghép cực giỏi ở nơi thiếu chi tiết, góc xoay lớn</div>
          <div style={{ fontSize: 25, color: danger }}>✗ Rất nặng, ngốn pin, chậm gấp 10-20 lần trên CPU</div>
          <div style={{ fontSize: 25, color: danger }}>✗ Có thể tự tin làm bậy làm vỡ toạc bản đồ!</div>
        </div>
      </Panel>
      <Panel tone="accent">
        <div style={titleStyle}>3. Hướng đi thông minh của Đề tài</div>
        <p style={bodyStyle}>
          Tại sao phải chọn 1 trong 2 khi ta có thể lấy ưu điểm của cả hai?
        </p>
        <div
          style={{
            marginTop: 'auto',
            background: 'rgba(255,159,67,0.10)',
            borderLeft: '3px solid var(--osd-accent)',
            padding: '16px 20px',
            fontSize: 25,
            lineHeight: 1.5,
          }}
        >
          <strong>Hệ thống thích ứng rủi ro:</strong> Bình thường cứ chạy Cổ điển cho mát máy. Khi phát hiện sắp vỡ bản đồ thì mới gọi AI giải cứu!
        </div>
      </Panel>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 04: Data / EDA
 * ------------------------------------------------------------------ */
const DataEda: Page = () => (
  <div style={page}>
    <Head
      n="03"
      label="DỮ LIỆU THỰC TẾ"
      title="Hai địa hình đối lập: Ruộng làng quê vs Bãi cỏ trơn"
      sub="Tại sao máy tính rất thích bay qua ruộng nhà cửa nhưng lại sợ bãi cỏ?"
    />
    <div style={{ marginTop: 40, display: 'grid', gridTemplateColumns: '1.15fr 1fr', gap: 40, flex: 1, minHeight: 0 }}>
      <div>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <Th w={300}>Đặc tính dữ liệu</Th>
              <Th>phantom3-village (Ruộng)</Th>
              <Th>phantom3-grass (Cỏ)</Th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <Td strong>Độ nét & Kênh màu</Td>
              <Td>Full HD 1080p (RGB)</Td>
              <Td>Full HD 1080p (RGB)</Td>
            </tr>
            <tr>
              <Td strong>Độ cao bay ước tính</Td>
              <Td>~194 mét (Cảnh phẳng)</Td>
              <Td>Bay lượn sát đất</Td>
            </tr>
            <tr>
              <Td strong>Số lượng ảnh chụp</Td>
              <Td>406 tấm (Bay dài 7.6 km)</Td>
              <Td>648 tấm (Bay lượn cục bộ)</Td>
            </tr>
            <tr>
              <Td strong>Khoảng cách giữa 2 ảnh</Td>
              <Td>18.9 m / bước (Bay rất nhanh)</Td>
              <Td>0.8 m / bước (Bay rất chậm)</Td>
            </tr>
            <tr>
              <Td strong>Đặc điểm nhìn bằng mắt</Td>
              <Td>
                <Verdict tone="ok">NHIỀU NHÀ CỬA, GÓC CẠNH</Verdict>
              </Td>
              <Td>
                <Verdict tone="bad">TOÀN CỎ XANH ĐỒNG NHẤT</Verdict>
              </Td>
            </tr>
            <tr>
              <Td strong>Thách thức khi dán ảnh</Td>
              <Td>Dễ tìm điểm nối, nhưng dễ trôi góc</Td>
              <Td tone={danger} strong>Cực khó: Rất dễ nối nhầm lá cỏ</Td>
            </tr>
          </tbody>
        </table>
        <p style={{ fontSize: 24, lineHeight: 1.5, color: muted, marginTop: 22 }}>
          💡 <strong>Ý nghĩa thực tế:</strong> Cảnh ruộng (`village`) giúp kiểm tra độ trôi góc quay khi bay nhanh.
          Cảnh cỏ (`grass`) là &quot;điểm yếu chí mạng&quot; kiểm tra xem thuật toán có bị lừa khi mặt đất không có chi tiết hay không.
        </p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22, minHeight: 0 }}>
        <div
          style={{
            position: 'relative',
            borderRadius: 'var(--osd-radius)',
            overflow: 'hidden',
            border: `1px solid ${line}`,
            flex: 1,
            minHeight: 0,
          }}
        >
          <img
            src={new URL('./assets/sample_village.jpg', import.meta.url).href}
            alt="Mẫu ảnh phantom3-village"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '12px 18px',
              background: 'rgba(11,15,20,0.88)',
              fontSize: 22,
              color: 'var(--osd-text)',
            }}
          >
            Ruộng đồng village: Nhiều bờ ruộng, mái nhà rõ rệt
          </div>
        </div>
        <div
          style={{
            position: 'relative',
            borderRadius: 'var(--osd-radius)',
            overflow: 'hidden',
            border: `1px solid ${line}`,
            flex: 1,
            minHeight: 0,
          }}
        >
          <img
            src={new URL('./assets/sample_grass.jpg', import.meta.url).href}
            alt="Mẫu ảnh phantom3-grass"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '12px 18px',
              background: 'rgba(11,15,20,0.88)',
              fontSize: 22,
              color: 'var(--osd-text)',
            }}
          >
            Bãi cỏ grass: Toàn màu xanh trơn nhẵn, rất dễ match nhầm
          </div>
        </div>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 05: 7-model benchmark & ca vỡ bản đồ
 * ------------------------------------------------------------------ */
const Benchmark: Page = () => (
  <div style={page}>
    <Head
      n="04"
      label="KHẢO SÁT 7 MÔ HÌNH"
      title="Nghịch lý thực tế: AI tự báo số liệu đẹp nhưng kéo rách bản đồ!"
      sub="Cùng dán 20 tấm ảnh: Xem thực tế mắt người nhìn thấy so với số liệu AI tự báo cáo"
    />
    <div style={{ marginTop: 40, display: 'grid', gridTemplateColumns: '1fr 1.05fr', gap: 40, flex: 1, minHeight: 0 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 26 }}>
        <Panel tone="bad">
          <div style={titleStyle}>1. AI tự báo cáo: Số liệu đẹp như mơ!</div>
          <p style={bodyStyle}>
            Mô hình AI <strong>EfficientLoFTR</strong> báo cáo nối được hơn <strong>2.000 điểm chuẩn</strong>,
            sai số khớp điểm nội tại siêu nhỏ (đẹp hơn cả thuật toán SIFT cổ điển!).
          </p>
        </Panel>
        <Panel tone="bad">
          <div style={titleStyle}>2. Mắt người nhìn thấy: Rách toạc bản đồ!</div>
          <p style={bodyStyle}>
            Nhìn sang hình bên phải: Khung ảnh bị kéo dãn xiên xẹo thành một vệt chéo dị dạng,
            diện tích bản đồ hữu ích tụt dốc thê thảm xuống chỉ còn <strong>55.6%</strong>!
          </p>
        </Panel>
        <Panel tone="accent">
          <div style={titleStyle}>3. Đúc kết đắt giá cho đề tài</div>
          <p style={bodyStyle}>
            <strong>Đừng bao giờ tin vào số lượng điểm nối:</strong> AI tự tin nối nhiều điểm không đồng nghĩa với việc dán đúng!
            Phải nhìn vào toàn bộ bản đồ tích luỹ mới phát hiện được sai số.
          </p>
        </Panel>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 22, minHeight: 0 }}>
        <div
          style={{
            position: 'relative',
            borderRadius: 'var(--osd-radius)',
            overflow: 'hidden',
            border: `2px solid ${danger}`,
            flex: 1,
            minHeight: 0,
          }}
        >
          <img
            src={new URL('./assets/mosaic_loftr_broken.png', import.meta.url).href}
            alt="Mosaic vỡ của EfficientLoFTR"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '12px 18px',
              background: 'rgba(11,15,20,0.92)',
              fontSize: 22,
              display: 'flex',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ color: danger, fontWeight: 700 }}>EfficientLoFTR: Bản đồ bị vặn rách (Phủ 55%)</span>
            <span style={{ color: muted, fontFamily: mono }}>Biến dạng chéo</span>
          </div>
        </div>
        <div
          style={{
            position: 'relative',
            borderRadius: 'var(--osd-radius)',
            overflow: 'hidden',
            border: `2px solid ${ok}`,
            flex: 1,
            minHeight: 0,
          }}
        >
          <img
            src={new URL('./assets/mosaic_sift.png', import.meta.url).href}
            alt="Mosaic SIFT baseline"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: 0,
              left: 0,
              right: 0,
              padding: '12px 18px',
              background: 'rgba(11,15,20,0.92)',
              fontSize: 22,
              display: 'flex',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ color: ok, fontWeight: 700 }}>SIFT cổ điển: Ghép thẳng thớm, chuẩn đẹp (Phủ 98%)</span>
            <span style={{ color: muted, fontFamily: mono }}>Vuông vắn</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 06: Chain vs Direct
 * ------------------------------------------------------------------ */
const Metric: Page = () => (
  <div style={page}>
    <Head
      n="05"
      label="CÂY THƯỚC ĐO ĐỘ TRÔI"
      title="Tự chế thước đo chuẩn: So 'Đi vòng dán dồn' với 'Đi thẳng 1 phát'"
      sub="Toạ độ GPS từ dataset có nhiều lỗi, nhóm tự thiết kế giải thuật đo hình học (Chain vs Direct)"
    />
    <div style={{ marginTop: 40, display: 'grid', gridTemplateColumns: '1fr 1.25fr', gap: 40, flex: 1, minHeight: 0 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Panel>
          <div style={titleStyle}>1. Bẫy dữ liệu GPS trong dataset</div>
          <p style={bodyStyle}>
            Toạ độ trong dataset thực chất do <strong>thuật toán SLAM tự đoán từ ảnh</strong>, không phải GPS đo độc lập.
            Ở cảnh cỏ nó còn bị lỗi chia cho 0 nên không thể làm Ground Truth chuẩn.
          </p>
        </Panel>
        <Panel tone="accent">
          <div style={titleStyle}>2. Thước đo tự chế: Chain vs Direct</div>
          <p style={bodyStyle}>
            - <strong>Đi vòng (Chain):</strong> Dán dồn 20 tấm liên tiếp (sai số cộng dồn).<br />
            - <strong>Đi thẳng (Direct):</strong> Lấy thẳng tấm 0 dán trực tiếp với tấm 19 (1 phát ăn ngay).<br />
            👉 Lệch nhau bao nhiêu pixel trên 5 điểm mốc = <strong>Độ trôi tích luỹ (Drift)</strong>.
          </p>
        </Panel>
        <Panel>
          <div style={titleStyle}>3. Bằng chứng số liệu đanh thép</div>
          <p style={bodyStyle}>
            Mức nhiễu nền của SIFT là 46.7 px. Riêng <strong>EfficientLoFTR trôi tới 1.311 pixel</strong> (gấp 28 lần mức nhiễu), chính thức bị kết tội làm vỡ bản đồ bằng số liệu!
          </p>
        </Panel>
      </div>
      <div>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <Th>Mô hình thử nghiệm</Th>
              <Th>Drift Ruộng village (frame 19)</Th>
              <Th>Drift Cỏ grass (frame 6)</Th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <Td strong>sift_bf (Mức nhiễu nền)</Td>
              <Td>46.7 px</Td>
              <Td>1.7 px</Td>
            </tr>
            <tr>
              <Td strong>sift_lightglue</Td>
              <Td>47.0 px</Td>
              <Td>1.8 px</Td>
            </tr>
            <tr>
              <Td strong>xfeat_lighterglue</Td>
              <Td>47.6 px</Td>
              <Td>3.4 px</Td>
            </tr>
            <tr>
              <Td strong>superpoint_lightglue</Td>
              <Td>61.1 px</Td>
              <Td>1.8 px</Td>
            </tr>
            <tr>
              <Td strong>orb_bf</Td>
              <Td>73.2 px</Td>
              <Td>2.8 px</Td>
            </tr>
            <tr>
              <Td strong tone={danger}>
                efficientloftr
              </Td>
              <Td tone={danger} strong>
                1.311,5 px (Gấp 28×)
              </Td>
              <Td tone={danger} strong>
                62.9 px (Gấp 37×)
              </Td>
            </tr>
          </tbody>
        </table>
        <p style={{ fontSize: 24, lineHeight: 1.5, color: muted, marginTop: 20 }}>
          💡 <strong>Cách đọc bảng:</strong> Dòng SIFT (46.7 px) là độ rung tự nhiên của thước đo. Các mô hình dao động 40-73 px có chất lượng tương đương nhau; riêng EfficientLoFTR vỡ nát hoàn toàn.
        </p>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 07: Kiến trúc đề xuất
 * ------------------------------------------------------------------ */
const Architecture: Page = () => (
  <div style={page}>
    <Head
      n="06"
      label="GIẢI PHÁP ĐỀ XUẤT"
      title="Hệ thống Đèn giao thông 3 tầng: Nhanh: Chuẩn: Tự cứu"
      sub="Bình thường chạy nhẹ (Đèn xanh) ➔ Rủi ro gọi AI cứu (Đèn vàng) ➔ AI bó tay thì tách mảnh (Đèn đỏ)"
    />
    <div style={{ marginTop: 40, display: 'flex', flexDirection: 'column', gap: 26, flex: 1, minHeight: 0 }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26, flex: 1, minHeight: 0 }}>
        <Panel tone="accent">
          <Crumb n="TẦNG 1" label="ĐÈN XANH · BẮT BỆNH" />
          <div style={titleStyle}>Dán nhanh bằng SIFT rồi soi màu</div>
          <p style={bodyStyle}>
            Cứ chạy SIFT cổ điển cho máy mát và siêu nhanh (0.07s/ảnh). Dán xong thì soi màu vùng đè lên nhau (Photo-NCC).
          </p>
          <div
            style={{
              marginTop: 'auto',
              fontFamily: mono,
              fontSize: 22,
              background: 'rgba(0,0,0,0.35)',
              padding: '12px 14px',
              borderRadius: 8,
              color: 'var(--osd-accent)',
            }}
          >
            Nếu lệch màu (NCC &lt; 0.93)
            <br />
            ➔ Bật Đèn Vàng báo động!
          </div>
        </Panel>
        <Panel tone="ok">
          <Crumb n="TẦNG 2" label="ĐÈN VÀNG · CỨU VIỆN" />
          <div style={titleStyle}>Chỉ gọi AI xịn ở bước bị cảnh báo</div>
          <p style={bodyStyle}>
            Bước an toàn: Dán tiếp luôn. Bước báo động: Kích hoạt SuperPoint + LightGlue ứng cứu riêng bước đó (1.2s) để vượt qua vùng hiểm trở.
          </p>
          <div
            style={{
              marginTop: 'auto',
              fontFamily: mono,
              fontSize: 22,
              background: 'rgba(0,0,0,0.35)',
              padding: '12px 14px',
              borderRadius: 8,
              color: ok,
            }}
          >
            Khớp chuẩn ➔ Dán tiếp
            <br />
            Tiết kiệm 80% thời gian!
          </div>
        </Panel>
        <Panel tone="bad">
          <Crumb n="TẦNG 3" label="ĐÈN ĐỎ · TỰ CỨU" />
          <div style={titleStyle}>Cắt mảnh để không vỡ cả bản đồ</div>
          <p style={bodyStyle}>
            Nếu sau khi gọi AI mà vẫn hỏng (mặt cỏ mất vân 100%): Chủ động cắt chuỗi, đóng gói mảnh cũ và mở mảnh bản đồ con mới (Submosaic), cô lập lỗi hoàn toàn!
          </p>
          <div
            style={{
              marginTop: 'auto',
              fontFamily: mono,
              fontSize: 22,
              background: 'rgba(0,0,0,0.35)',
              padding: '12px 14px',
              borderRadius: 8,
              color: danger,
            }}
          >
            Bảo toàn 100% video
            <br />
            Không bị vỡ nát dây chuyền!
          </div>
        </Panel>
      </div>
      <div
        style={{
          background: surface,
          border: `1px solid ${line}`,
          borderLeft: '3px solid var(--osd-accent)',
          borderRadius: 'var(--osd-radius)',
          padding: '24px 34px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: 24,
        }}
      >
        <span style={{ color: muted }}>Bình thường (84%)</span>
        <span style={{ fontFamily: mono, color: ok, fontWeight: 700 }}>SIFT nhẹ · 0.07 s/ảnh</span>
        <span style={{ color: 'var(--osd-accent)', fontSize: 30 }}>➔</span>
        <span style={{ color: muted }}>Báo động (16%)</span>
        <span style={{ fontFamily: mono, color: 'var(--osd-accent)', fontWeight: 700 }}>AI LightGlue · 1.2 s</span>
        <span style={{ color: danger, fontSize: 30 }}>➔</span>
        <span style={{ color: muted }}>Vẫn hỏng nặng</span>
        <span style={{ fontFamily: mono, color: danger, fontWeight: 700 }}>Tách Submosaic (Giữ 100%)</span>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 08: RQ1 kết quả
 * ------------------------------------------------------------------ */
const Rq1: Page = () => (
  <div style={page}>
    <Head
      n="07"
      label="KẾT QUẢ RQ1 · BẮT BỆNH"
      title="Đếm điểm nối không báo được lỗi: So sánh màu sắc mới phát hiện chuẩn!"
      sub="Thực nghiệm 45 bước thực tế: Đếm điểm nối đạt AUC 0.40 (tệ hơn tung đồng xu), màu sắc đạt AUC 0.85"
    />
    <div style={{ marginTop: 38, display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: 40, flex: 1, minHeight: 0 }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <Th>Chỉ số kiểm tra</Th>
            <Th w={140}>Tương quan ρ</Th>
            <Th w={150}>AUC bắt lỗi</Th>
            <Th w={230}>Đánh giá thực tế</Th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <Td strong>photo_bad_frac (Lệch màu)</Td>
            <Td>+0.759</Td>
            <Td strong>0.855</Td>
            <Td>
              <Verdict tone="ok">BẮT BỆNH NHẠY NHẤT</Verdict>
            </Td>
          </tr>
          <tr>
            <Td strong>rmse_px (Sai số RANSAC)</Td>
            <Td>+0.788</Td>
            <Td strong>0.839</Td>
            <Td>
              <Verdict tone="accent">DỄ BỊ LỪA BỞI AI</Verdict>
            </Td>
          </tr>
          <tr>
            <Td strong>overlap_ratio (Vùng chồng)</Td>
            <Td>-0.634</Td>
            <Td strong>0.788</Td>
            <Td>
              <Verdict tone="ok">RẤT TỐT</Verdict>
            </Td>
          </tr>
          <tr>
            <Td strong>photo_ncc (Tương quan màu)</Td>
            <Td>-0.636</Td>
            <Td strong>0.770</Td>
            <Td>
              <Verdict tone="ok">CHỌN LÀM NGƯỠNG</Verdict>
            </Td>
          </tr>
          <tr>
            <Td strong>inlier_ratio (Tỷ lệ chuẩn)</Td>
            <Td>-0.389</Td>
            <Td>0.726</Td>
            <Td>Dự phòng phụ</Td>
          </tr>
          <tr>
            <Td strong>hull_area_ratio (Độ trải điểm)</Td>
            <Td>+0.005</Td>
            <Td>0.571</Td>
            <Td>Gần như đoán mò</Td>
          </tr>
          <tr>
            <Td strong>inliers (Số điểm chuẩn)</Td>
            <Td>+0.239</Td>
            <Td tone={danger} strong>
              0.409
            </Td>
            <Td>
              <Verdict tone="bad">NGƯỢC CHIỀU (TỆ)</Verdict>
            </Td>
          </tr>
          <tr>
            <Td strong>matches (Số điểm nối)</Td>
            <Td>+0.251</Td>
            <Td tone={danger} strong>
              0.402
            </Td>
            <Td>
              <Verdict tone="bad">HOÀN TOÀN VÔ DỤNG</Verdict>
            </Td>
          </tr>
        </tbody>
      </table>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Panel tone="bad">
          <div style={titleStyle}>Tại sao đếm điểm lại vô dụng?</div>
          <p style={bodyStyle}>
            Khi bay qua bãi cỏ, mô hình AI tìm được hơn 2.000 điểm nối giả giữa các lá cỏ giống hệt nhau.
            Máy tính tưởng là nhiều điểm nên rất tự tin, nhưng thực chất đang bẻ cong cả bản đồ!
          </p>
        </Panel>
        <Panel tone="ok">
          <div style={titleStyle}>Tại sao màu sắc (Photo-NCC) lại cực nhạy?</div>
          <p style={bodyStyle}>
            Sau khi ốp ảnh mới vào ảnh cũ, ta lấy màu sắc trừ cho nhau: Nếu dán đúng, mái nhà đè lên mái nhà (màu khớp khít).
            Nếu dán lệch, mái nhà đè lên ruộng lúa ➔ Màu sắc lệch tông vọt lên ngay lập tức!
          </p>
        </Panel>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 09: RQ2 kết quả
 * ------------------------------------------------------------------ */
const Rq2: Page = () => (
  <div style={page}>
    <Head
      n="08"
      label="KẾT QUẢ RQ2 · PHÂN LUỒNG"
      title="Lạm dụng AI 100% không tối ưu: Vừa chậm gấp 19 lần vừa méo bản đồ!"
      sub="Chỉ bật AI ở 16% bước khó: Giảm 62% độ trôi và chạy nhanh gấp 4.5 lần so với bật AI liên tục"
    />
    <div style={{ marginTop: 38, display: 'grid', gridTemplateColumns: '1.35fr 1fr', gap: 40, flex: 1, minHeight: 0 }}>
      <div>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <Th>Chính sách phân luồng</Th>
              <Th w={150}>Tỷ lệ gọi AI</Th>
              <Th w={140}>Thời gian</Th>
              <Th w={160}>Độ trôi bản đồ</Th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <Td strong>1. Chỉ dùng SIFT nhẹ</Td>
              <Td>0% (0/45)</Td>
              <Td>3.2 giây</Td>
              <Td>75.3 px</Td>
            </tr>
            <tr style={{ background: 'rgba(239,68,68,0.08)' }}>
              <Td strong tone={danger}>
                2. Bật AI 100% (LightGlue)
              </Td>
              <Td>100% (45/45)</Td>
              <Td tone={danger} strong>60.4 giây</Td>
              <Td tone={danger} strong>
                82.4 px (TỆ HƠN!)
              </Td>
            </tr>
            <tr class="highlight-row">
              <Td strong tone="var(--osd-accent)">
                3. Phân luồng thông minh (τ=0.93)
              </Td>
              <Td strong>16% (7/45 bước)</Td>
              <Td strong>13.3 giây</Td>
              <Td strong tone={ok}>
                28.5 px (TỐT NHẤT)
              </Td>
            </tr>
            <tr>
              <Td strong>4. Phân luồng + Leo thang 1080p</Td>
              <Td>16% (7/45 bước)</Td>
              <Td>73.6 giây</Td>
              <Td>35.8 px</Td>
            </tr>
          </tbody>
        </table>
        <Panel tone="accent">
          <div style={titleStyle}>💡 Phát hiện mấu chốt cho bài báo:</div>
          <p style={bodyStyle}>
            - <strong>AI không phải thuốc tiên:</strong> Bắt AI chạy mọi lúc vừa tốn pin vừa làm bản đồ trôi tới 82.4 px (do đặc trưng thô ở 640px tích tụ sai số).<br />
            - <strong>Phân luồng thích ứng:</strong> Chỉ gọi AI ở 16% bước khó, bản đồ vừa đẹp nhất (28.5 px) vừa chạy nhanh gấp 4.5 lần so với chạy AI toàn phần!
          </p>
        </Panel>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Panel>
          <div style={titleStyle}>Quét lưới tìm điểm tối ưu Pareto</div>
          <p style={bodyStyle}>
            Nhóm quét ngưỡng từ 0.90 đến 0.99 với ngân sách leo thang tối đa 25%:
            Tại τ = 0.93, hệ thống chỉ leo thang đúng 7 bước hiểm trở nhất, đạt mức trôi thấp nhất toàn bộ thực nghiệm (28.5 px).
          </p>
        </Panel>
        <Panel tone="ok">
          <div style={titleStyle}>Ablation Study: Ảnh nhỏ vs Ảnh gốc</div>
          <p style={bodyStyle}>
            Tại 7 bước khó, nếu gọi AI xử lý ảnh gốc 1080p thì sai số bước cực nhỏ (1.49 px vs 4.51 px), nhưng tổng thời gian tăng vọt lên 73 giây.
            Phân luồng ở 640px là lựa chọn tối ưu cho máy tính cá nhân.
          </p>
        </Panel>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 10: RQ3 kết quả
 * ------------------------------------------------------------------ */
const Rq3: Page = () => (
  <div style={page}>
    <Head
      n="09"
      label="KẾT QUẢ RQ3 · TỰ CỨU"
      title="Bỏ ảnh khi gặp lỗi làm mất dữ liệu: Tách mảnh mới cứu được bản đồ!"
      sub="So sánh 4 chiến lược cứu nguy: Vứt ảnh gây sụp đổ dây chuyền làm mất trắng 70% video"
    />
    <div style={{ marginTop: 38, display: 'grid', gridTemplateColumns: '1.35fr 1fr', gap: 40, flex: 1, minHeight: 0 }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <Th>Kịch bản địa hình</Th>
            <Th w={230}>Chiến lược cứu nguy</Th>
            <Th w={130}>Ảnh giữ</Th>
            <Th w={120}>Số mảnh</Th>
            <Th w={150}>Độ trôi</Th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <Td strong>Ruộng village (SIFT)</Td>
            <Td>1. Không cứu (Mặc kệ)</Td>
            <Td>46/46</Td>
            <Td>1</Td>
            <Td>84.6 px</Td>
          </tr>
          <tr>
            <Td strong>Ruộng village (SIFT)</Td>
            <Td tone={danger}>2. Bỏ ảnh (Drop frame)</Td>
            <Td tone={danger} strong>14/46</Td>
            <Td>1</Td>
            <Td>21.7 px (Mất 70% video)</Td>
          </tr>
          <tr>
            <Td strong>Ruộng village (SIFT)</Td>
            <Td tone={danger}>3. Ghép ảnh mốc cũ</Td>
            <Td tone={danger} strong>14/46</Td>
            <Td>1</Td>
            <Td>21.7 px (Mất 70% video)</Td>
          </tr>
          <tr class="highlight-row">
            <Td strong>Ruộng village (SIFT)</Td>
            <Td tone={ok} strong>
              4. Tách Submosaic
            </Td>
            <Td tone={ok} strong>
              46/46 (100%)
            </Td>
            <Td strong>8</Td>
            <Td strong tone={ok}>21.7 px (Bảo toàn)</Td>
          </tr>
          <tr>
            <Td strong>Bãi cỏ grass (LoFTR vỡ)</Td>
            <Td>Không cứu</Td>
            <Td>46/46</Td>
            <Td>1</Td>
            <Td tone={danger}>671.3 px (Vỡ nát)</Td>
          </tr>
          <tr class="highlight-row">
            <Td strong>Bãi cỏ grass (LoFTR vỡ)</Td>
            <Td tone={ok} strong>
              Tách Submosaic
            </Td>
            <Td>46/46</Td>
            <Td tone={danger}>45</Td>
            <Td>2.7 px / mảnh</Td>
          </tr>
        </tbody>
      </table>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Panel tone="bad">
          <div style={titleStyle}>⚠️ Bẫy sụp đổ dây chuyền (Cascade Failure)</div>
          <p style={bodyStyle}>
            Vứt 1 tấm ảnh ➔ Khoảng cách tới tấm sau xa gấp đôi ➔ Tấm sau càng khó ghép hơn ➔ Lại tiếp tục vứt.
            Từ 7 cảnh báo ban đầu nở thành 32 lần vứt ảnh, làm mất trắng 70% video khảo sát!
          </p>
        </Panel>
        <Panel tone="ok">
          <div style={titleStyle}>Tách Submosaic là giải pháp tối ưu</div>
          <p style={bodyStyle}>
            Khi gặp đoạn quá khó: Chủ động cắt chuỗi, coi đoạn trước là một mảnh bản đồ con sạch sẽ và bắt đầu mảnh mới.
            Kết quả: <strong>Giữ trọn vẹn 100% video (46/46 tấm)</strong>, độ trôi nội bộ mỗi mảnh chỉ 21.7 px!
          </p>
        </Panel>
      </div>
    </div>
  </div>
);
const Timeline: Page = () => (
  <div style={page}>
    <Head
      n="10"
      label="TIẾN ĐỘ & BẰNG CHỨNG"
      title="Nhật ký thực hiện trong học kỳ & Kế hoạch Paper IEEE"
      sub="Mỗi tuần đều có bằng chứng code chạy thực tế và nhật ký nghiệm thu rõ ràng"
    />
    <div style={{ marginTop: 40, display: 'grid', gridTemplateColumns: '1.3fr 1fr', gap: 40, flex: 1, minHeight: 0 }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <Th w={170}>Thời gian</Th>
            <Th>Công việc nhóm đã hoàn thành</Th>
            <Th w={280}>Bằng chứng thực tế</Th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <Td strong>Tuần 1-3</Td>
            <Td>Khảo sát văn hiến, nộp đề cương Proposal</Td>
            <Td>Proposal · RDR-0001 → 0005</Td>
          </tr>
          <tr>
            <Td strong>Tuần 4-5</Td>
            <Td>Dựng pipeline cổ điển & thử nghiệm LightGlue</Td>
            <Td>Notebook 01 & Notebook 02</Td>
          </tr>
          <tr>
            <Td strong>Tuần 6-7</Td>
            <Td>Chạy đua 7 mô hình, phát hiện ca vỡ LoFTR</Td>
            <Td>Notebook 03 · Báo cáo HTML</Td>
          </tr>
          <tr>
            <Td strong>Tuần 8</Td>
            <Td>Kiểm chứng toạ độ, chế tạo thước đo tự thân</Td>
            <Td>Notebook 04 · RDR-0007</Td>
          </tr>
          <tr>
            <Td strong>Tuần 9</Td>
            <Td>Hiện thực hoá 3 RQ, audit code & sweep ngưỡng</Td>
            <Td tone={ok} strong>Notebook 05 · RDR-0008 (Verified)</Td>
          </tr>
        </tbody>
      </table>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <Panel tone="accent">
          <div style={titleStyle}>Kế hoạch viết Paper IEEE (Giai đoạn 3)</div>
          <p style={bodyStyle}>
            1. Đưa số liệu thực nghiệm đã kiểm chứng từ Notebook 05 vào 3 bảng kết quả chuẩn IEEE.<br />
            2. Trích dẫn 18 bài báo nòng cốt đã phân loại (theo quyết định RDR-0009).<br />
            3. Hoàn thiện bản thảo LaTeX tối thiểu 4 trang theo yêu cầu học phần.
          </p>
        </Panel>
        <Panel>
          <div style={titleStyle}>Thử nghiệm mở rộng</div>
          <p style={bodyStyle}>
            Đo kiểm chứng tính tổng quát của ngưỡng rủi ro τ = 0.93 trên thêm 1-2 gói dữ liệu khác của NPU Drone-Map.
          </p>
        </Panel>
      </div>
    </div>
  </div>
);

/* ------------------------------------------------------------------ *
 * 12: Kết
 * ------------------------------------------------------------------ */
const Closing: Page = () => (
  <div
    style={{
      ...fill,
      background: 'var(--osd-bg)',
      color: 'var(--osd-text)',
      padding: '0 150px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
    }}
  >
    <div style={{ fontFamily: mono, fontSize: 24, color: 'var(--osd-accent)', letterSpacing: '0.14em' }}>
      TỔNG KẾT BÁO CÁO PRESENT 2
    </div>
    <h2
      style={{
        fontFamily: 'var(--osd-font-display)',
        fontSize: 72,
        fontWeight: 850,
        lineHeight: 1.15,
        letterSpacing: '-0.02em',
        margin: '26px 0 44px',
        maxWidth: 1550,
      }}
    >
      3 Bài học cốt lõi cho một hệ thống ghép ảnh UAV thực tế
    </h2>
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28, maxWidth: 1520 }}>
      <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
        <span style={{ fontFamily: mono, fontSize: 28, fontWeight: 700, color: 'var(--osd-accent)' }}>01</span>
        <p style={{ fontSize: 28, lineHeight: 1.5, margin: 0, color: 'var(--osd-text)' }}>
          <strong>Đừng tin số lượng điểm nối:</strong> AI tìm được 2.000 điểm chuẩn vẫn có thể kéo rách toạc bản đồ.
          Chỉ có kiểm tra màu sắc sau khi dán mới vạch trần được lỗi.
        </p>
      </div>
      <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
        <span style={{ fontFamily: mono, fontSize: 28, fontWeight: 700, color: 'var(--osd-accent)' }}>02</span>
        <p style={{ fontSize: 28, lineHeight: 1.5, margin: 0, color: 'var(--osd-text)' }}>
          <strong>Bật AI 100% là dại dột:</strong> Chậm gấp 19 lần mà bản đồ trôi nặng hơn.
          Chỉ bật AI ở 16% bước khó giúp giảm 62% độ trôi và chạy nhanh gấp 4.5 lần.
        </p>
      </div>
      <div style={{ display: 'flex', gap: 24, alignItems: 'baseline' }}>
        <span style={{ fontFamily: mono, fontSize: 28, fontWeight: 700, color: 'var(--osd-accent)' }}>03</span>
        <p style={{ fontSize: 28, lineHeight: 1.5, margin: 0, color: 'var(--osd-text)' }}>
          <strong>Bỏ ảnh khi gặp lỗi là cách xử lý sai lầm:</strong> Gây sụp đổ dây chuyền làm mất trắng 70% video.
          Tách mảnh bản đồ con (Submosaic) là cách duy nhất bảo toàn 100% dữ liệu khảo sát.
        </p>
      </div>
    </div>
    <div
      style={{
        marginTop: 52,
        borderTop: `1px solid ${line}`,
        paddingTop: 26,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontSize: 24,
        color: muted,
      }}
    >
      <span style={{ color: '#fff', fontWeight: 600 }}>Cảm ơn Quý Thầy Cô và các bạn đã lắng nghe!</span>
      <span style={{ fontFamily: mono, fontSize: 20 }}>
        Bằng chứng thực nghiệm: <span style={{ color: ok }}>notebooks/01 → 05 (Verified)</span>
      </span>
    </div>
  </div>
);

export const meta: SlideMeta = {
  title: 'Failure-Aware 2D Aerial Mosaicking: Present 2',
  createdAt: '2026-10-14T07:56:39.449Z',
};

export default [
  Cover,
  Problem,
  RelatedWorks,
  DataEda,
  Benchmark,
  Metric,
  Architecture,
  Rq1,
  Rq2,
  Rq3,
  Timeline,
  Closing,
] satisfies Page[];

export const notes: (string | undefined)[] = [
  // 1: Cover
  `Chào Thầy Cô và các bạn. Nhóm xin trình bày đề tài: Ghép ảnh flycam tự phát hiện lỗi và tự sửa sai theo thời gian thực.
Hiểu nôm na: Flycam bay trên trời chụp hàng trăm tấm ảnh rời rạc. Nhiệm vụ của nhóm là dán chúng lại thành một bản đồ lớn mà không bị méo, không làm đơ máy và tự cứu khi gặp lỗi.`,

  // 2: Problem
  `Bài toán này có một cái bẫy chết người: Sai một ly, đi một dặm!
Tưởng tượng dán 45 tấm ảnh liên tiếp: Tấm thứ 5 chỉ cần dán lệch nhẹ 2 độ, đến tấm 45 cả bản đồ sẽ bị vặn rách toạc.
Đề tài giải quyết 3 câu hỏi sinh viên hiểu ngay: Bắt bệnh ghép sai (RQ1) -> Gọi AI cứu viện (RQ2) -> Cứu nguy bản đồ (RQ3).`,

  // 3: Related works
  `Trước đây có 2 thái cực đều chưa tối ưu:
Cổ điển (SIFT/ORB) chạy rất nhẹ nhưng mù khi gặp bãi cỏ trơn nhẵn.
Học sâu (AI) rất thông minh nhưng ngốn pin, chậm gấp 19 lần và có thể tự tin làm bậy.
Nhóm lấy ưu điểm cả hai: Bình thường chạy nhẹ cho mát máy, gặp chỗ nguy hiểm mới gọi AI!`,

  // 4: Data
  `Hai kịch bản thử nghiệm đối lập hoàn toàn:
Ruộng village nhiều góc nhà mái ngói rất dễ tìm điểm nối, nhưng bay nhanh nên dễ trôi góc.
Bãi cỏ grass toàn màu xanh trơn nhẵn, là điểm yếu chí mạng của máy tính vì rất dễ nối nhầm lá cỏ này sang lá cỏ khác.`,

  // 5: Benchmark
  `Phát hiện chấn động ở Notebook 03:
Mô hình AI EfficientLoFTR tự khen mình tìm được 2.000 điểm chuẩn, sai số nội tại siêu nhỏ.
Nhưng nhìn mắt thường bên phải: Bản đồ bị kéo rách toạc, diện tích phủ rớt xuống còn 55%!
Đúc kết đắt giá: Đừng bao giờ tin vào điểm số nội tại của AI!`,

  // 6: Metric
  `File toạ độ GPS trong dữ liệu có nhiều bẫy và bị lỗi chia cho 0, nhóm tự chế cây thước đo chuẩn Chain vs Direct:
So sánh: Đi vòng dán 20 tấm dồn lại (Chain) với Đi thẳng lấy tấm 0 dán 1 phát ăn ngay với tấm 19 (Direct).
Lệch nhau bao nhiêu pixel = Độ trôi tích luỹ. Vạch trần EfficientLoFTR trôi tới 1.311 pixel (gấp 28 lần mức nhiễu của SIFT)!`,

  // 7: Architecture
  `Giải pháp của nhóm là hệ thống đèn giao thông 3 tầng:
Đèn xanh: Dán nhanh bằng SIFT nhẹ (0.07s/ảnh). Dán xong soi màu sắc (Photo-NCC).
Đèn vàng: Lệch màu (NCC < 0.93) -> Gọi AI LightGlue ứng cứu riêng bước đó (1.2s). Khớp chuẩn thì dán tiếp.
Đèn đỏ: AI vẫn bó tay -> Tách mảnh bản đồ con (Submosaic) để cô lập lỗi, không để hỏng cả bản đồ.`,

  // 8: RQ1
  `Đếm số điểm nối là vô dụng (AUC 0.40, tệ hơn tung đồng xu đoán mò).
So sánh màu sắc sau khi dán mới bắt đúng bệnh (AUC 0.85): Mái nhà đè lên ruộng lúa là màu sắc lệch tông vọt lên ngay lập tức!`,

  // 9: RQ2
  `Lạm dụng AI cho mọi ảnh không hề tối ưu: Chậm gấp 19 lần mà bản đồ trôi tới 82 px.
Chỉ bật AI ở 16% bước khó: Giảm 62% độ trôi (xuống 28.5 px) và chạy nhanh gấp 4.5 lần so với bật AI liên tục!`,

  // 10: RQ3
  `Bỏ ảnh khi gặp lỗi là cách xử lý sai lầm: Vứt 1 ảnh làm rụng dây chuyền mất trắng 70% video!
Tách mảnh bản đồ con (Submosaic): Cắt chuỗi rủi ro, bảo toàn trọn vẹn 100% video khảo sát (46/46 tấm).`,

  // 11: Timeline
  `Nhật ký học kỳ: 5 mốc tiến độ đều có code chạy thực tế và kiểm chứng tại Notebook 01 -> 05.
Kế hoạch Giai đoạn 3: Viết bài báo IEEE tối thiểu 4 trang LaTeX với 18 tài liệu nòng cốt đã phân loại.`,

  // 12: Closing
  `3 bài học thực tế đúc kết cho một hệ thống ghép ảnh UAV:
1. Đừng tin số lượng điểm nối của AI.
2. Bật AI 100% vừa chậm vừa méo bản đồ.
3. Tách submosaic là cách duy nhất cứu vãn 100% dữ liệu bay.
Cảm ơn Quý Thầy Cô và các bạn đã chú ý lắng nghe!`,
];
