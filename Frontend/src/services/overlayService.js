import apiClient from './apiClient';

export const overlayService = {
  getOverlayState(overlayToken) {
    return apiClient.get(`/overlay/state/${overlayToken}`).then((r) => r.data);
  },
  updateOverlayState({ overlay_token, current_state, payload }) {
    return apiClient.post('/overlay/state', { overlay_token, current_state, payload }).then((r) => r.data);
  },
  hideOverlay(overlayToken) {
    return apiClient.post('/overlay/hide', { overlay_token: overlayToken }).then((r) => r.data);
  },
};
