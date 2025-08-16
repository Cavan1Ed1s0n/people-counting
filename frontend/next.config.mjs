/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  experimental: {
    serverActions: { allowedOrigins: ["*"] },
  },
  images: { remotePatterns: [{ protocol: "http", hostname: "**" }, { protocol: "https", hostname: "**" }] }
};
export default nextConfig;
