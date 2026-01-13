import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  ActivityIndicator, 
  KeyboardAvoidingView, 
  Platform,
  ScrollView,
  StatusBar
} from 'react-native';
import { useAuthStore } from '../../stores/useAuthStore';
import { useNavigation } from '@react-navigation/native';
import { 
  User, 
  Mail, 
  Lock, 
  ChevronLeft, 
  GraduationCap, 
  CarFront, // Ou use 'Car' se sua versão do lucide for mais antiga
  CheckCircle2
} from 'lucide-react-native';

export const RegisterScreen = () => {
  const navigation = useNavigation();
  const { signUp, isLoading, error } = useAuthStore();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState<'student' | 'instructor'>('student');

  const handleRegister = async () => {
    if(!fullName || !email || !password) return;
    
    await signUp({
      email,
      password,
      full_name: fullName,
      user_type: userType // Usando o campo correto
    });
  };

  // Componente Auxiliar para o Card de Seleção
  const TypeCard = ({ type, icon: Icon, title, description }: any) => {
    const isSelected = userType === type;
    return (
      <TouchableOpacity 
        onPress={() => setUserType(type)}
        className={`flex-1 p-4 rounded-2xl border-2 transition-all mr-2 ${
          isSelected 
            ? 'border-primary bg-indigo-50' 
            : 'border-slate-100 bg-white'
        }`}
      >
        <View className="flex-row justify-between items-start">
          <Icon 
            size={24} 
            color={isSelected ? '#4F46E5' : '#94A3B8'} 
            strokeWidth={isSelected ? 2.5 : 2}
          />
          {isSelected && <CheckCircle2 size={16} color="#4F46E5" />}
        </View>
        <Text className={`mt-3 font-bold text-base ${isSelected ? 'text-primary' : 'text-slate-600'}`}>
          {title}
        </Text>
        <Text className="text-xs text-slate-400 mt-1 leading-4">
          {description}
        </Text>
      </TouchableOpacity>
    );
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-background"
    >
      <StatusBar barStyle="dark-content" backgroundColor="#F8FAFC" />
      
      {/* Header com Botão Voltar */}
      <View className="px-6 pt-12 pb-4">
        <TouchableOpacity 
          onPress={() => navigation.goBack()}
          className="w-10 h-10 bg-white items-center justify-center rounded-full shadow-sm border border-slate-100"
        >
          <ChevronLeft color="#0F172A" size={24} />
        </TouchableOpacity>
      </View>

      <ScrollView 
        contentContainerStyle={{ flexGrow: 1, paddingHorizontal: 24, paddingBottom: 40 }}
        showsVerticalScrollIndicator={false}
      >
        
        {/* Títulos */}
        <View className="mb-8">
          <Text className="text-3xl font-extrabold text-slate-900">
            Criar conta
          </Text>
          <Text className="text-slate-500 mt-2 text-base">
            Junte-se ao UDrive e comece sua jornada.
          </Text>
        </View>

        {/* Seletor de Tipo (Cards Lado a Lado) */}
        <View className="flex-row mb-8">
          <TypeCard 
            type="student" 
            icon={GraduationCap} 
            title="Sou Aluno" 
            description="Quero encontrar instrutores e aprender."
          />
          <View className="w-4" /> 
          <TypeCard 
            type="instructor" 
            icon={CarFront} 
            title="Sou Instrutor" 
            description="Quero gerenciar aulas e conseguir alunos."
          />
        </View>

        {/* Formulário */}
        <View className="space-y-5">
          
          {/* Input Nome */}
          <View>
            <Text className="text-slate-700 font-semibold mb-2 ml-1 text-sm">Nome Completo</Text>
            <View className="flex-row items-center bg-white border border-slate-200 rounded-xl px-4 h-14 focus:border-primary">
              <User color="#94A3B8" size={20} />
              <TextInput 
                className="flex-1 ml-3 text-slate-800 font-medium"
                placeholder="Ex: Carlos Silva"
                placeholderTextColor="#CBD5E1"
                value={fullName}
                onChangeText={setFullName}
              />
            </View>
          </View>

          {/* Input Email */}
          <View>
            <Text className="text-slate-700 font-semibold mb-2 ml-1 text-sm">Email</Text>
            <View className="flex-row items-center bg-white border border-slate-200 rounded-xl px-4 h-14">
              <Mail color="#94A3B8" size={20} />
              <TextInput 
                className="flex-1 ml-3 text-slate-800 font-medium"
                placeholder="seu@email.com"
                placeholderTextColor="#CBD5E1"
                keyboardType="email-address"
                autoCapitalize="none"
                value={email}
                onChangeText={setEmail}
              />
            </View>
          </View>

          {/* Input Senha */}
          <View>
            <Text className="text-slate-700 font-semibold mb-2 ml-1 text-sm">Senha</Text>
            <View className="flex-row items-center bg-white border border-slate-200 rounded-xl px-4 h-14">
              <Lock color="#94A3B8" size={20} />
              <TextInput 
                className="flex-1 ml-3 text-slate-800 font-medium"
                placeholder="••••••••"
                placeholderTextColor="#CBD5E1"
                secureTextEntry
                value={password}
                onChangeText={setPassword}
              />
            </View>
            <Text className="text-xs text-slate-400 mt-1 ml-1">
              Mínimo de 6 caracteres
            </Text>
          </View>
        </View>

        {/* Mensagem de Erro */}
        {error && (
          <View className="bg-red-50 p-4 rounded-xl border border-red-100 mt-6 flex-row items-center">
            <View className="w-1 h-8 bg-red-400 rounded-full mr-3" />
            <Text className="text-red-500 font-medium flex-1">{error}</Text>
          </View>
        )}

        {/* Botão Principal */}
        <TouchableOpacity 
          className={`bg-primary rounded-xl py-4 mt-8 shadow-lg shadow-indigo-500/30 flex-row justify-center items-center ${isLoading ? 'opacity-70' : ''}`}
          onPress={handleRegister}
          disabled={isLoading}
        >
          {isLoading ? (
            <ActivityIndicator color="#FFF" />
          ) : (
            <>
              <Text className="text-white font-bold text-lg mr-2">Cadastrar</Text>
              {/* Seta para direita sutil no botão */}
              <ChevronLeft size={20} color="#FFF" style={{ transform: [{ rotate: '180deg' }]}} />
            </>
          )}
        </TouchableOpacity>

        {/* Rodapé */}
        <View className="mt-8 mb-4 items-center">
          <Text className="text-slate-400 text-sm">
            Ao se cadastrar, você concorda com nossos
          </Text>
          <View className="flex-row mt-1">
            <Text className="text-primary font-semibold text-sm">Termos de Uso</Text>
            <Text className="text-slate-400 text-sm mx-1">e</Text>
            <Text className="text-primary font-semibold text-sm">Privacidade</Text>
          </View>
        </View>

      </ScrollView>
    </KeyboardAvoidingView>
  );
};