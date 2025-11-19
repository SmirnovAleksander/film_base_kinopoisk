import { cookies } from 'next/headers';
import { STORAGE_KEYS } from '@/lib/config';

export async function getServerAuthToken() {
    const cookieStore = await cookies();
    return cookieStore.get(STORAGE_KEYS.AUTH_TOKEN)?.value;
}
