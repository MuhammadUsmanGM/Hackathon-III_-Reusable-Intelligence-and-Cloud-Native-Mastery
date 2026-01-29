import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, context } = body;

    // Simulate AI tutor response - in real implementation, this would call the backend AI service
    const aiResponse = {
      role: 'assistant',
      content: `I received your message: "${message}". As your Python tutor, I can help explain concepts, debug code, or provide exercises. This is a simulated response from the backend AI service.`,
      timestamp: new Date().toISOString(),
      context: {
        ...context,
        lastInteraction: new Date().toISOString()
      }
    };

    return NextResponse.json(aiResponse);
  } catch (error) {
    console.error('Error in AI tutor API:', error);
    return NextResponse.json(
      { error: 'Failed to process your request' },
      { status: 500 }
    );
  }
}