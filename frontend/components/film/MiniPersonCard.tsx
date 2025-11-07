'use client';

import Image from 'next/image';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ROUTES } from '@/lib/config';

interface MiniPersonCardProps {
  person: {
    id: number;
    name?: string | null;
    original_name?: string | null;
    image?: string | null;
    career?: string[];
    profession?: string;
    profession_key?: string;
  };
  className?: string;
}

export function MiniPersonCard({ person, className = '' }: MiniPersonCardProps) {
  const displayName = person.name || person.original_name || 'Неизвестно';
  const displayOriginalName = person.original_name && person.name !== person.original_name ? person.original_name : null;

  return (
    <Card className={`group hover:shadow-md transition-all duration-200 p-0 ${className}`}>
      <CardContent className="p-3">
        <div className="flex items-center space-x-3">
          {/* Фото */}
          <div className="shrink-0">
            {person.image ? (
              <div className="w-16 h-16 rounded-lg overflow-hidden bg-muted">
                <Image
                  src={person.image}
                  alt={displayName}
                  width={64}
                  height={64}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                  unoptimized={false}
                />
              </div>
            ) : (
              <div className="w-16 h-16 rounded-lg bg-muted flex items-center justify-center">
                <span className="text-muted-foreground text-xs text-center px-1">
                  Нет фото
                </span>
              </div>
            )}
          </div>

          {/* Информация */}
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-sm leading-tight mb-1 line-clamp-2">
              <Link
                href={ROUTES.STUFF_DETAILS(person.id)}
                className="hover:text-primary transition-colors"
              >
                {displayName}
              </Link>
            </h3>
            
            {displayOriginalName && (
              <p className="text-xs text-muted-foreground mb-1 line-clamp-1">
                {displayOriginalName}
              </p>
            )}
            
            {person.career && person.career.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {person.career.slice(0, 2).map((role, index) => (
                  <Badge key={index} variant="secondary" className="text-xs px-1 py-0">
                    {role}
                  </Badge>
                ))}
                {person.career.length > 2 && (
                  <Badge variant="outline" className="text-xs px-1 py-0">
                    +{person.career.length - 2}
                  </Badge>
                )}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}