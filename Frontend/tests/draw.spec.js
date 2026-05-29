/** @vitest-environment jsdom */
import { shallowMount } from '@vue/test-utils';
import { describe, expect, it, vi } from 'vitest';
import { nextTick } from 'vue';

vi.mock('@/services/raffleService', () => ({
  raffleService: {
    create: vi.fn(),
    calculateScore: vi.fn(),
    selectWinner: vi.fn(),
    startClaim: vi.fn(),
  },
}));

vi.mock('@/services/participantService', () => ({
  participantService: {
    listByRaffle: vi.fn(() => Promise.resolve({ data: [] })),
    bulkCreate: vi.fn(),
  },
}));

vi.mock('@/services/overlayService', () => ({
  overlayService: {
    getMyOverlay: vi.fn(),
    updateOverlayState: vi.fn(),
  },
}));

vi.mock('@/stores/twitchStore', () => ({
  useTwitchStore: () => ({ connected: true, refreshConnection: vi.fn(() => Promise.resolve()) }),
}));

vi.mock('@/stores/authStore', () => ({
  useAuthStore: () => ({ token: 'unit-test-token', user: { id: 'user-1' }, loadTokenFromStorage: vi.fn() }),
}));

import Draw from '../src/views/Dashboard/draw.vue';

function mountDraw() {
  return shallowMount(Draw, {
    global: {
      mocks: {
        $router: { push: vi.fn(() => Promise.resolve()) },
      },
      stubs: {
        AnimacionSorteo: true,
      },
    },
  });
}

describe('draw.vue raffle lifecycle', () => {
  it('prepareNewRaffle clears the raffle lifecycle state', async () => {
    const wrapper = mountDraw();
    await nextTick();

    const stopParticipantsPollingSpy = vi.spyOn(wrapper.vm, 'stopParticipantsPolling');

    await wrapper.setData({
      raffleId: 'raffle-1',
      winner: 'winner',
      participants: [{ username: 'one' }],
      manualParticipants: [{ username: 'two' }],
      backendParticipants: [{ username: 'three' }],
      raffleFinished: true,
      hasWinnerSelected: true,
      twitchStore: { connected: true },
    });

    wrapper.vm.prepareNewRaffle();
    await nextTick();

    expect(stopParticipantsPollingSpy).toHaveBeenCalled();
    expect(wrapper.vm.raffleId).toBeNull();
    expect(wrapper.vm.winner).toBe('');
    expect(wrapper.vm.participants).toEqual([]);
    expect(wrapper.vm.manualParticipants).toEqual([]);
    expect(wrapper.vm.backendParticipants).toEqual([]);
    expect(wrapper.vm.raffleFinished).toBe(false);
    expect(wrapper.vm.hasWinnerSelected).toBe(false);
  });

  it('disables the draw button and shows finalization text when the raffle is finished', async () => {
    const wrapper = mountDraw();
    await nextTick();

    await wrapper.setData({ raffleId: 'raffle-1', raffleFinished: true, hasWinnerSelected: false });

    const drawButton = wrapper.findAll('button').find((button) => button.text() === 'Sorteo finalizado');
    expect(drawButton.exists()).toBe(true);
    expect(drawButton.attributes('disabled')).toBeDefined();
  });

  it('disables the draw button and shows finalization text when a winner was selected', async () => {
    const wrapper = mountDraw();
    await nextTick();

    await wrapper.setData({ raffleId: 'raffle-1', raffleFinished: false, hasWinnerSelected: true });

    const drawButton = wrapper.findAll('button').find((button) => button.text() === 'Sorteo finalizado');
    expect(drawButton.exists()).toBe(true);
    expect(drawButton.attributes('disabled')).toBeDefined();
  });
});
