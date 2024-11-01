'use client'

import { useState, useEffect } from 'react';
import axios from 'axios';
import DOMPurify from 'dompurify';
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { marked } from 'marked';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Gavel, Menu, Send, User, Moon, Sun, LogOut, PlusCircle, Car, Building2, Timer, UserPlus, Phone, Video, Scale, HelpCircle, MessageSquare } from 'lucide-react';

const promptMappings = [
  { title: "Know Your Case Status", prompt: "Can you give me the case status with diary no 1212 and diary year 2013?", icon: Gavel },
  { title: "Pending Cases in India", prompt: "How much is the age-wise pending case status in India?", icon: Scale },
  { title: "Traffic Violation", prompt: "How to file E-challan in India?", icon: Car },
  { title: "eCourts Services in India", prompt: "Tell me more about court services in India", icon: Building2 },
  { title: "Fast Track Court in India", prompt: "Fast track court services in India", icon: Timer },
  { title: "Judge Appointment in India", prompt: "What is the procedure for judges' appointments in India?", icon: UserPlus },
  { title: "Tele-Law in India", prompt: "Tele_Law_Services", icon: Phone },
  { title: "Watch Live Streaming of Supreme Court", prompt: "Current live stream of court cases in the Supreme Court", icon: Video },
];




export default function Component() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [showWelcome, setShowWelcome] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [showCaseForm, setShowCaseForm] = useState(false);
  const [caseDetails, setCaseDetails] = useState({ diaryNo: '', diaryYear: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    document.body.classList.toggle('dark', isDarkMode);
  }, [isDarkMode]);

  const handleSend = async () => {
    if (inputValue.trim()) {
      setMessages(prev => [...prev, { type: 'user', content: inputValue }]);
      const query = inputValue;
      setInputValue('');
      setShowWelcome(false);
      setIsLoading(true);

      console.log(process.env.BACKEND_URL)

      try {
        const response = await axios({
          method: 'post',
          url: "http://127.0.0.1:8000",
          data: { query },
          headers: { 'Content-Type': 'application/json' }
        });
        
        const answer = response.data.answer;
        setMessages(prev => [...prev, { type: 'bot', content: answer }]);
      } catch (error) {
        console.log("Error fetching data: ", error);
        setMessages(prev => [...prev, { type: 'bot', content: "Sorry, I couldn't process your request." }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const renderMessageContent = (content) => {
    // Parse markdown to HTML
    const rawHtml = marked(content);
    // Sanitize HTML to prevent XSS
    const sanitizedHtml = DOMPurify.sanitize(rawHtml);
    
    return (
      <div 
        className="prose dark:prose-invert"
        dangerouslySetInnerHTML={{ __html: sanitizedHtml }} 
      />
    );
  };

  const handleQuickPrompt = (prompt) => {
    if (prompt === 'Know Your Case Status') {
      setShowCaseForm(true);
    } else {
      setInputValue(prompt);
      setShowWelcome(false);
      handleSend();
    }
  };

  const handleCaseSubmit = () => {
    const prompt = `Give me the case summary of Diary No ${caseDetails.diaryNo} and Diary Year ${caseDetails.diaryYear}`;
    setInputValue(prompt);
    setShowCaseForm(false);
    handleSend();
  };

  return (
    <div className={`flex flex-col h-screen ${isDarkMode ? 'dark bg-gray-900 text-white' : 'bg-purple-50'}`}>
      {/* Header */}
      <header className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 border-b dark:border-gray-700">
        <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="w-6 h-6" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px] sm:w-[400px]">
            <SheetHeader>
              <SheetTitle>Chat History</SheetTitle>
            </SheetHeader>
            <div className="py-4">
              <Button onClick={() => setMessages([])} className="w-full mb-4 bg-purple-600 hover:bg-purple-700 text-white">
                <PlusCircle className="mr-2 h-4 w-4" /> New Chat
              </Button>
            </div>
          </SheetContent>
        </Sheet>
        
        <div className="flex items-center gap-2">
          <Gavel className="w-6 h-6 text-purple-600 dark:text-purple-400" />
          <span className="text-xl font-semibold text-purple-600 dark:text-purple-400">NyayDost</span>
        </div>

        <div className="flex items-center gap-2">
          <Dialog open={showHelp} onOpenChange={setShowHelp}>
            <DialogTrigger asChild>
              <Button variant="ghost" size="icon">
                <HelpCircle className="w-6 h-6" />
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>How to Use NyayDost</DialogTitle>
              </DialogHeader>
              <div className="space-y-4 py-4">
                <h3 className="font-semibold">Quick Start Guide:</h3>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Use the quick access cards on the homepage for common legal queries</li>
                  <li>Type your specific questions in the chat input</li>
                  <li>Access case status by providing Diary Number and Year</li>
                  <li>View chat history from the sidebar menu</li>
                  <li>Toggle between light and dark mode for comfort</li>
                </ul>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  NyayDost is designed to provide general legal information. For specific legal advice, please consult a qualified legal professional.
                </p>
              </div>
            </DialogContent>
          </Dialog>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <User className="w-6 h-6" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onSelect={() => setIsDarkMode(!isDarkMode)}>
                {isDarkMode ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
                {isDarkMode ? 'Light' : 'Dark'} Mode
              </DropdownMenuItem>
              <DropdownMenuItem>
                <MessageSquare className="mr-2 h-4 w-4" />
                Help us improve
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <LogOut className="mr-2 h-4 w-4" /> Logout
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {showWelcome ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <h1 className="text-4xl font-bold mb-4">Hi, I am NyayDost</h1>
            <p className="text-xl mb-8">Your AI legal assistant</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl w-full mb-8">
              {promptMappings.map((item, index) => (
                <Card 
                  key={index}
                  className="cursor-pointer hover:bg-purple-100 transition-colors"
                  onClick={() => handleQuickPrompt(item.prompt)}
                >
                  <CardContent className="p-4 text-center space-y-2">
                    <item.icon className="w-8 h-8 mx-auto text-purple-600" />
                    <h3 className="font-medium text-sm">{item.title}</h3>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-lg ${message.type === 'user' ? 'bg-purple-600 text-white dark:bg-purple-700 rounded-br-none' : 'bg-white text-gray-800 dark:bg-gray-700 dark:text-white rounded-bl-none'}`}>
                  {renderMessageContent(message.content)}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-[80%] p-3 rounded-lg bg-white text-gray-800 dark:bg-gray-700 dark:text-white rounded-bl-none">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white dark:bg-gray-800 border-t dark:border-gray-700">
        {showCaseForm && (
          <Dialog open={showCaseForm} onOpenChange={setShowCaseForm}>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Enter Case Details</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="diaryNo">Diary Number</Label>
                  <Input 
                    id="diaryNo" 
                    value={caseDetails.diaryNo} 
                    onChange={(e) => setCaseDetails({ ...caseDetails, diaryNo: e.target.value })} 
                    placeholder="Enter Diary Number" 
                  />
                </div>
                <div>
                  <Label htmlFor="diaryYear">Diary Year</Label>
                  <Input 
                    id="diaryYear" 
                    value={caseDetails.diaryYear} 
                    onChange={(e) => setCaseDetails({ ...caseDetails, diaryYear: e.target.value })} 
                    placeholder="Enter Diary Year" 
                  />
                </div>
                <Button onClick={handleCaseSubmit}>Submit</Button>
              </div>
            </DialogContent>
          </Dialog>
        )}
        <div className="flex">
          <Input 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
            placeholder="Type your message..."
            className="flex-1 mr-2"
          />
          <Button onClick={handleSend} disabled={!inputValue.trim()}>
            <Send className="w-6 h-6" />
          </Button>
        </div>
      </div>
    </div>
  );
}