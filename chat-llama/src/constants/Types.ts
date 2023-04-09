export type Sources = 'user' | 'server';

export interface DiscussionItem {
  source: Sources;
  text?: string;
}
