export function normalizeUsername(value) {
  return (value || '')
    .toLowerCase()
    .trim()
    .replace(/^@+/, '')
    .replace(/\s+/g, '_')
    .replace(/_+/g, '_');
}

export function getParticipantKey(participant) {
  const username = normalizeUsername(
    participant?.username || participant?.name || participant?.display_name || participant,
  );
  return username ? `username:${username}` : '';
}

export function dedupeParticipantsForDraw(list = []) {
  const deduped = new Map();
  list.forEach((participant) => {
    const key = getParticipantKey(participant);
    if (!key) return;
    deduped.set(key, participant);
  });
  return Array.from(deduped.values());
}

export function prepareNewRaffleState() {
  return {
    raffleId: null,
    confirmationMode: null,
    drawError: '',
    drawSuccess: '',
    manualInput: '',
    isStopped: false,
    raffleFinished: false,
    hasWinnerSelected: false,
    isRaffleRunning: false,
    isSyncingParticipants: false,
    winner: '',
    backendParticipants: [],
    manualParticipants: [],
    participants: [],
    manualParticipantsSynced: false,
    mostrarAnimacion: false,
    isClaimStarted: false,
    claimExpiresAt: null,
    hoverIndex: -1,
  };
}
