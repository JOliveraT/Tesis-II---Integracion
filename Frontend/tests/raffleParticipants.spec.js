import { describe, expect, it } from 'vitest';
import {
  dedupeParticipantsForDraw,
  normalizeUsername,
  prepareNewRaffleState,
} from '../src/utils/raffleParticipants';

describe('raffle participant utilities', () => {
  it('normalizes usernames consistently', () => {
    expect(normalizeUsername('Test_front')).toBe('test_front');
    expect(normalizeUsername('test front')).toBe('test_front');
    expect(normalizeUsername('  @Test   Front  ')).toBe('test_front');
  });

  it('deduplicates participants by normalized username', () => {
    const participants = dedupeParticipantsForDraw([
      { username: 'test front', display_name: 'test front' },
      { username: 'Test_front', display_name: 'Test_front' },
    ]);

    expect(participants).toHaveLength(1);
    expect(normalizeUsername(participants[0].username)).toBe('test_front');
  });

  it('returns a clean state for preparing a new raffle', () => {
    expect(prepareNewRaffleState()).toMatchObject({
      raffleId: null,
      winner: '',
      participants: [],
      manualParticipants: [],
      backendParticipants: [],
      raffleFinished: false,
      hasWinnerSelected: false,
    });
  });
});
