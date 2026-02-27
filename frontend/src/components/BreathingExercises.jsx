import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

const exercises = [
  {
    id: 'box',
    name: 'Box Breathing',
    icon: '📦',
    description: 'Equal 4-count breathing for calm and focus',
    pattern: [
      { phase: 'Breathe In', duration: 4, color: 'from-blue-400 to-blue-600' },
      { phase: 'Hold', duration: 4, color: 'from-purple-400 to-purple-600' },
      { phase: 'Breathe Out', duration: 4, color: 'from-pink-400 to-pink-600' },
      { phase: 'Hold', duration: 4, color: 'from-indigo-400 to-indigo-600' },
    ]
  },
  {
    id: '478',
    name: '4-7-8 Relaxation',
    icon: '🧘',
    description: 'Deep relaxation breathing technique',
    pattern: [
      { phase: 'Breathe In', duration: 4, color: 'from-green-400 to-green-600' },
      { phase: 'Hold', duration: 7, color: 'from-teal-400 to-teal-600' },
      { phase: 'Breathe Out', duration: 8, color: 'from-cyan-400 to-cyan-600' },
    ]
  },
  {
    id: 'grounding',
    name: '5-4-3-2-1 Grounding',
    icon: '🌿',
    description: 'Sensory awareness to reduce anxiety',
    isGrounding: true
  }
];

const groundingSteps = [
  { count: 5, sense: 'See', prompt: 'Name 5 things you can see around you', color: 'blue' },
  { count: 4, sense: 'Touch', prompt: 'Name 4 things you can touch', color: 'purple' },
  { count: 3, sense: 'Hear', prompt: 'Name 3 things you can hear', color: 'pink' },
  { count: 2, sense: 'Smell', prompt: 'Name 2 things you can smell', color: 'indigo' },
  { count: 1, sense: 'Taste', prompt: 'Name 1 thing you can taste', color: 'green' },
];

function BreathingExercises({ setToken }) {
  const navigate = useNavigate();
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const [currentPhase, setCurrentPhase] = useState(0);
  const [countdown, setCountdown] = useState(0);
  const [cycles, setCycles] = useState(0);
  const [groundingStep, setGroundingStep] = useState(0);
  const [groundingItems, setGroundingItems] = useState([]);
  const [currentItem, setCurrentItem] = useState('');
  const audioContextRef = useRef(null);

  useEffect(() => {
    let interval;
    if (isActive && selectedExercise && !selectedExercise.isGrounding) {
      const pattern = selectedExercise.pattern;
      const phaseDuration = pattern[currentPhase].duration;
      
      if (countdown > 0) {
        interval = setInterval(() => {
          setCountdown(c => c - 1);
        }, 1000);
      } else if (countdown === 0 && isActive) {
        playTone();
        const nextPhase = (currentPhase + 1) % pattern.length;
        setCurrentPhase(nextPhase);
        setCountdown(pattern[nextPhase].duration);
        
        if (nextPhase === 0) {
          setCycles(c => c + 1);
        }
      }
    }
    return () => clearInterval(interval);
  }, [isActive, countdown, currentPhase, selectedExercise]);

  const playTone = () => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    const ctx = audioContextRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    oscillator.frequency.value = 440;
    gainNode.gain.value = 0.1;
    
    oscillator.start();
    setTimeout(() => oscillator.stop(), 100);
  };

  const startExercise = (exercise) => {
    setSelectedExercise(exercise);
    if (!exercise.isGrounding) {
      setCurrentPhase(0);
      setCountdown(exercise.pattern[0].duration);
      setCycles(0);
    } else {
      setGroundingStep(0);
      setGroundingItems([]);
    }
    setIsActive(true);
  };

  const stopExercise = () => {
    setIsActive(false);
    setSelectedExercise(null);
    setCycles(0);
    setGroundingStep(0);
    setGroundingItems([]);
    setCurrentItem('');
  };

  const addGroundingItem = () => {
    if (currentItem.trim()) {
      setGroundingItems([...groundingItems, currentItem]);
      setCurrentItem('');
      
      if (groundingItems.length + 1 >= groundingSteps[groundingStep].count) {
        if (groundingStep < groundingSteps.length - 1) {
          setGroundingStep(groundingStep + 1);
          setGroundingItems([]);
        } else {
          // Exercise complete
          setTimeout(() => {
            alert('🎉 Grounding exercise complete! You should feel more present and calm.');
            stopExercise();
          }, 500);
        }
      }
    }
  };

  const getCircleSize = () => {
    if (!selectedExercise || selectedExercise.isGrounding) return 0;
    const pattern = selectedExercise.pattern;
    const phaseDuration = pattern[currentPhase].duration;
    const progress = (phaseDuration - countdown) / phaseDuration;
    
    // Grow during breathe in and hold, shrink during breathe out
    if (pattern[currentPhase].phase.includes('In') || pattern[currentPhase].phase === 'Hold') {
      return 50 + (progress * 100); // Grow from 50% to 150%
    } else {
      return 150 - (progress * 100); // Shrink from 150% to 50%
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <Navbar setToken={setToken} />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-gray-600 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 mb-4 transition-colors duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Dashboard
          </button>

          <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
            🧘 Breathing Exercises
          </h1>
          <p className="text-gray-600 dark:text-gray-300 transition-colors duration-300">
            Quick relief techniques for stress and anxiety
          </p>
        </div>

        {!selectedExercise ? (
          /* Exercise Selection */
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {exercises.map(exercise => (
              <div
                key={exercise.id}
                onClick={() => startExercise(exercise)}
                className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 cursor-pointer transform transition-all duration-300 hover:scale-105 hover:shadow-2xl border-2 border-transparent hover:border-purple-500 dark:hover:border-purple-400"
              >
                <div className="text-6xl mb-4 text-center">{exercise.icon}</div>
                <h3 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-2 text-center transition-colors duration-300">
                  {exercise.name}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-center mb-4 transition-colors duration-300">
                  {exercise.description}
                </p>
                <button className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300">
                  Start Exercise
                </button>
              </div>
            ))}
          </div>
        ) : selectedExercise.isGrounding ? (
          /* 5-4-3-2-1 Grounding Exercise */
          <div className="max-w-2xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 transition-colors duration-300">
              <div className="text-center mb-8">
                <div className="text-6xl mb-4">🌿</div>
                <h2 className="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
                  5-4-3-2-1 Grounding
                </h2>
                <p className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                  Focus on your senses to ground yourself in the present
                </p>
              </div>

              <div className={`mb-8 p-6 rounded-xl bg-gradient-to-r ${
                groundingStep === 0 ? 'from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30' :
                groundingStep === 1 ? 'from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30' :
                groundingStep === 2 ? 'from-pink-100 to-pink-200 dark:from-pink-900/30 dark:to-pink-800/30' :
                groundingStep === 3 ? 'from-indigo-100 to-indigo-200 dark:from-indigo-900/30 dark:to-indigo-800/30' :
                'from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30'
              } transition-all duration-500`}>
                <div className="text-center">
                  <div className="text-5xl font-bold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
                    {groundingSteps[groundingStep].count}
                  </div>
                  <div className="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-2 transition-colors duration-300">
                    Things You Can {groundingSteps[groundingStep].sense}
                  </div>
                  <div className="text-gray-600 dark:text-gray-400 transition-colors duration-300">
                    {groundingSteps[groundingStep].prompt}
                  </div>
                </div>
              </div>

              <div className="mb-6">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={currentItem}
                    onChange={(e) => setCurrentItem(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addGroundingItem()}
                    placeholder={`Type something you ${groundingSteps[groundingStep].sense.toLowerCase()}...`}
                    className="flex-1 px-4 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 dark:bg-gray-700 dark:text-gray-100 transition-colors duration-300"
                  />
                  <button
                    onClick={addGroundingItem}
                    className="px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-300"
                  >
                    Add
                  </button>
                </div>
              </div>

              <div className="space-y-2 mb-6">
                {groundingItems.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg text-gray-800 dark:text-gray-200 transition-colors duration-300 animate-fade-in"
                  >
                    {idx + 1}. {item}
                  </div>
                ))}
              </div>

              <div className="flex gap-4">
                <button
                  onClick={stopExercise}
                  className="flex-1 bg-gray-500 text-white py-3 rounded-xl font-semibold hover:bg-gray-600 transition-colors duration-300"
                >
                  End Exercise
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Breathing Animation */
          <div className="max-w-2xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 transition-colors duration-300">
              <div className="text-center mb-8">
                <div className="text-5xl mb-4">{selectedExercise.icon}</div>
                <h2 className="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2 transition-colors duration-300">
                  {selectedExercise.name}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-4 transition-colors duration-300">
                  Cycles completed: <span className="font-bold text-purple-600 dark:text-purple-400">{cycles}</span>
                </p>
              </div>

              {/* Breathing Circle */}
              <div className="relative w-full aspect-square max-w-md mx-auto mb-8">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div
                    className={`rounded-full bg-gradient-to-br ${selectedExercise.pattern[currentPhase].color} transition-all duration-1000 ease-in-out shadow-2xl`}
                    style={{
                      width: `${getCircleSize()}%`,
                      height: `${getCircleSize()}%`,
                    }}
                  >
                    <div className="absolute inset-0 flex flex-col items-center justify-center text-white">
                      <div className="text-2xl font-bold mb-2">
                        {selectedExercise.pattern[currentPhase].phase}
                      </div>
                      <div className="text-6xl font-bold">
                        {countdown}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Pattern Timeline */}
              <div className="flex justify-center gap-2 mb-8">
                {selectedExercise.pattern.map((phase, idx) => (
                  <div
                    key={idx}
                    className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 ${
                      idx === currentPhase
                        ? 'bg-purple-600 text-white scale-110'
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                    }`}
                  >
                    {phase.phase} ({phase.duration}s)
                  </div>
                ))}
              </div>

              {/* Controls */}
              <div className="flex gap-4">
                <button
                  onClick={stopExercise}
                  className="flex-1 bg-red-500 text-white py-3 rounded-xl font-semibold hover:bg-red-600 transition-colors duration-300"
                >
                  Stop Exercise
                </button>
                <button
                  onClick={() => setIsActive(!isActive)}
                  className="flex-1 bg-purple-600 text-white py-3 rounded-xl font-semibold hover:bg-purple-700 transition-colors duration-300"
                >
                  {isActive ? 'Pause' : 'Resume'}
                </button>
              </div>

              {/* Tips */}
              <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg transition-colors duration-300">
                <p className="text-sm text-gray-700 dark:text-gray-300 transition-colors duration-300">
                  💡 <strong>Tip:</strong> Find a comfortable position, close your eyes if you'd like, 
                  and follow the breathing pattern. Sound cues will guide you.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default BreathingExercises;
