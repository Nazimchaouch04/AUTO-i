const shimmerStyle = {
  background: 'linear-gradient(90deg, #1C1C2E 25%, #252538 50%, #1C1C2E 75%)',
  backgroundSize: '200% 100%',
  animation: 'shimmer 1.8s infinite',
  borderRadius: 6,
};

export function SkeletonBox({ width = '100%', height = 16, radius = 6 }) {
  return <div style={{ ...shimmerStyle, width, height, borderRadius: radius }} />;
}

export function SkeletonCard() {
  return (
    <div style={{
      background: '#13131E', borderRadius: 12,
      padding: 16, border: '1px solid rgba(255,255,255,0.06)',
      display: 'flex', flexDirection: 'column', gap: 10,
    }}>
      <SkeletonBox height={14} width="55%" />
      <SkeletonBox height={10} width="35%" />
      <SkeletonBox height={40} radius={8} />
      <div style={{ display: 'flex', gap: 6 }}>
        <SkeletonBox height={24} width={60} radius={20} />
        <SkeletonBox height={24} width={60} radius={20} />
      </div>
      <SkeletonBox height={10} width="70%" />
    </div>
  );
}

export function SkeletonKPI() {
  return (
    <div style={{
      background: '#13131E', borderRadius: 12, padding: 20,
      border: '1px solid rgba(255,255,255,0.06)',
    }}>
      <SkeletonBox height={10} width="40%" style={{ marginBottom: 12 }} />
      <SkeletonBox height={28} width="60%" radius={4} />
    </div>
  );
}
