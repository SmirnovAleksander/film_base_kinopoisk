import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'avatars.mds.yandex.net',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'kinopoisk.ru',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: '*.yandex.net',
        pathname: '/**',
      },
      {
        protocol: 'https',
        hostname: 'encrypted-tbn0.gstatic.com',
        pathname: '/**',
      },
    ],
  },
};

export default nextConfig;
