import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axiosClient from '../api/axiosClient';

export function useAnnonces(filters = {}) {
  const params = new URLSearchParams(
    Object.fromEntries(Object.entries(filters).filter(([,v]) => v))
  ).toString();
  return useQuery({
    queryKey: ['annonces', filters],
    queryFn: () => axiosClient.get(`/api/annonces/?${params}`).then(r => r.data),
  });
}

export function useDashboardStats(period = '30') {
  return useQuery({
    queryKey: ['dashboard', period],
    queryFn: () => axiosClient.get(`/api/dashboard/stats/?period=${period}`).then(r => r.data),
    staleTime: 2 * 60 * 1000,
  });
}

export function useProfil() {
  return useQuery({
    queryKey: ['profil'],
    queryFn: () => axiosClient.get('/api/gamification/profil/').then(r => r.data),
    staleTime: 60 * 1000,
  });
}

export function useLeaderboard(type = 'global') {
  return useQuery({
    queryKey: ['leaderboard', type],
    queryFn: () => axiosClient.get(`/api/gamification/leaderboard/?type=${type}`).then(r => r.data),
    staleTime: 5 * 60 * 1000,
  });
}

export function useDefis() {
  return useQuery({
    queryKey: ['defis'],
    queryFn: () => axiosClient.get('/api/gamification/defis/').then(r => r.data),
    staleTime: 60 * 1000,
  });
}

export function useAlertes() {
  return useQuery({
    queryKey: ['alertes'],
    queryFn: () => axiosClient.get('/api/alertes/').then(r => r.data),
  });
}

export function useAnnonceDetail(id) {
  return useQuery({
    queryKey: ['annonce', id],
    queryFn: () => axiosClient.get(`/api/annonces/${id}/`).then(r => r.data),
    enabled: !!id,
  });
}

export function useEstimation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => axiosClient.post('/api/estimation/', data).then(r => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profil'] });
    },
  });
}
