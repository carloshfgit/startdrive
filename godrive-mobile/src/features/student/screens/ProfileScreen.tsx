import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useAuthStore } from '../../stores/useAuthStore';

export const ProfileScreen = () => {
  const signOut = useAuthStore((state) => state.signOut);

  return (
    <View className="flex-1 bg-background justify-center items-center">
      <Text className="text-text-primary text-xl font-bold mb-6">Meu Perfil</Text>
      
      <TouchableOpacity 
        onPress={signOut}
        className="bg-red-50 px-6 py-3 rounded-xl border border-red-100"
      >
        <Text className="text-red-500 font-semibold">Sair da Conta</Text>
      </TouchableOpacity>
    </View>
  );
};