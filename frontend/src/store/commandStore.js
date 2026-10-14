import { create } from 'zustand';

export const useCommandStore = create((set, get) => ({
    commands: JSON.parse(localStorage.getItem('commandHistory')) || [],
    favorites: JSON.parse(localStorage.getItem('favorites')) || [],
    currentCommand: '',
    lastResult: null,
    isExecuting: false,
    error: null,

    addCommand: (command) => {
        const commands = get().commands;
        const updated = [command, ...commands.filter(c => c !== command)].slice(0, 50);
        localStorage.setItem('commandHistory', JSON.stringify(updated));
        set({ commands: updated });
    },

    toggleFavorite: (command) => {
        const favorites = get().favorites;
        const updated = favorites.includes(command)
            ? favorites.filter(c => c !== command)
            : [command, ...favorites];
        localStorage.setItem('favorites', JSON.stringify(updated));
        set({ favorites: updated });
    },

    setCurrentCommand: (command) => set({ currentCommand: command }),
    setLastResult: (result) => set({ lastResult: result }),
    setIsExecuting: (isExecuting) => set({ isExecuting }),
    setError: (error) => set({ error }),
    clearError: () => set({ error: null }),
}));
