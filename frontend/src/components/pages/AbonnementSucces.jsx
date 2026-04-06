import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { fetchProfile } from '../../store/userSlice';
import { CheckCircle, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function AbonnementSucces() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    // Declencher l'animation
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#FFE159', '#FFFFFF', '#4CAF50']
    });

    // Mettre a jour le profil
    if (sessionId) {
      dispatch(fetchProfile());
    }
  }, [dispatch, sessionId]);

  return (
    <div className="min-h-screen bg-[#0D0D14] flex flex-col items-center justify-center p-4">
      <div className="border border-success/20 bg-success/5 p-10 rounded-[3rem] max-w-xl w-full text-center animate-fade-in-up">
        <div className="w-24 h-24 bg-success/20 rounded-full flex items-center justify-center mx-auto mb-8 border-4 border-success/30">
          <CheckCircle className="w-12 h-12 text-success" />
        </div>
        
        <h1 className="text-4xl font-black text-white mb-4">
          Félicitations !
        </h1>
        <p className="text-xl text-primary-text-secondary mb-8">
          Vous êtes maintenant AutoIntel Pro. Merci de votre confiance !
        </p>
        
        <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-8 inline-block w-full">
          <p className="text-lg font-bold text-accent mb-2">🎁 +200 AutoCoins offerts</p>
          <p className="text-sm text-primary-text-secondary">Ils ont été crédités sur votre compte.</p>
        </div>

        <button 
          onClick={() => navigate('/dashboard')}
          className="w-full bg-accent text-white font-black py-4 px-8 rounded-2xl flex items-center justify-center gap-3 hover:scale-[1.02] transition-transform"
        >
          Découvrir mes nouveaux avantages <ArrowRight size={20} />
        </button>
      </div>

      <style jsx>{`
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up { animation: fade-in-up 0.6s ease-out forwards; }
      `}</style>
    </div>
  );
}
