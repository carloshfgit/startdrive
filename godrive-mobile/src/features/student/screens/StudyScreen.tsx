import React from 'react';
import { View, Text } from 'react-native';

export const StudyScreen = () => {
  return (
    <View className="flex-1 bg-background justify-center items-center">
      <Text className="text-text-primary text-xl font-bold">Módulo de Estudo</Text>
      <Text className="text-text-secondary mt-2">Em breve: Cursos e Simulados</Text>
    </View>
  );
};