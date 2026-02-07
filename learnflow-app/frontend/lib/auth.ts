
import { createAuthClient } from "better-auth/react";

/**
 * Better Auth Client Configuration
 * This implements the required standard for authentication in the Hackathon.
 */
export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
});

export const { 
    signIn, 
    signUp, 
    signOut, 
    useSession 
} = authClient;
