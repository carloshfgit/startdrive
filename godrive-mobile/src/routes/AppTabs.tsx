import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, GraduationCap, User } from 'lucide-react-native';

// Import das telas
import { HomeScreen } from '../screens/student/HomeScreen';
import { StudyScreen } from '../screens/student/StudyScreen';
import { ProfileScreen } from '../screens/student/ProfileScreen';

const Tab = createBottomTabNavigator();

export function AppTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false, // Oculta o header padrão do React Navigation
        tabBarShowLabel: true, // Mostra o nome da aba (Instrutores, Estudar...)
        tabBarActiveTintColor: '#4F46E5', // Indigo-600 (Cor do ícone ativo)
        tabBarInactiveTintColor: '#94A3B8', // Slate-400 (Cor do ícone inativo)
        tabBarStyle: {
          backgroundColor: '#FFFFFF', // Fundo branco
          borderTopColor: '#F1F5F9', // Borda sutil
          paddingBottom: 8, // Espaçamento para iPhone X+
          paddingTop: 8,
          height: 60,
          elevation: 5, // Sombra no Android
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        }
      }}
    >
      <Tab.Screen 
        name="Instructors" 
        component={HomeScreen} 
        options={{
          tabBarLabel: 'Instrutores',
          tabBarIcon: ({ color, size }) => (
            <Home color={color} size={size} />
          ),
        }}
      />

      <Tab.Screen 
        name="Study" 
        component={StudyScreen} 
        options={{
          tabBarLabel: 'Estudar',
          tabBarIcon: ({ color, size }) => (
            <GraduationCap color={color} size={size} />
          ),
        }}
      />

      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen} 
        options={{
          tabBarLabel: 'Perfil',
          tabBarIcon: ({ color, size }) => (
            <User color={color} size={size} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}