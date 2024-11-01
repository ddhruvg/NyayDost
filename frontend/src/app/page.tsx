'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent } from "@/components/ui/card"
import { Gavel, HelpCircle, Menu, Send, User, Moon, Sun, LogOut, PlusCircle, Scale, Car, Building2, Timer, UserPlus, Phone, Video } from 'lucide-react'

const promptMappings = [
  {
    title: "Know Your Case Status",
    prompt: "Can you give me the case status in India?",
    icon: Gavel
  },
  {
    title: "Pending Cases in India",
    prompt: "How much is the age-wise pending case status in India?",
    icon: Scale
  },
  {
    title: "Traffic Violation",
    prompt: "Traffic_Violation_and_E_Challan",
    icon: Car
  },
  {
    title: "eCourts Services in India",
    prompt: "Tell me more about court services in India",
    icon: Building2
  },
  {
    title: "Fast Track Court in India",
    prompt: "Fast track court services in India",
    icon: Timer
  },
  {
    title: "Judge Appointment in India",
    prompt: "What is the procedure for judges' appointments in India?",
    icon: UserPlus
  },
  {
    title: "Tele-Law in India",
    prompt: "Tele_Law_Services",
    icon: Phone
  },
  {
    title: "Watch Live Streaming of Supreme Court",
    prompt: "Current live stream of court cases in the Supreme Court",
    icon: Video
  }
]

export default function Component() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [showWelcome, setShowWelcome] = useState(true)
  const [showInput, setShowInput] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [chatSessions, setChatSessions] = useState([
    { id: 1, title: "Case Status Inquiry" },
    { id: 2, title: "Legal Advice on Property" },
    { id: 3, title: "Court Procedure Question" },
  ])
  const [showCaseForm, setShowCaseForm] = useState(false)
  const [caseDetails, setCaseDetails] = useState({ diaryNo: '', diaryYear: '' })
  const [showCourtSelect, setShowCourtSelect] = useState(false)
  const [selectedCourt, setSelectedCourt] = useState('')

  useEffect(() => {
    document.body.classList.toggle('dark', isDarkMode)
  }, [isDarkMode])

  const handleSend = () => {
    if (inputValue.trim()) {
      //@ts-ignore
      setMessages([...messages, { type: 'user', content: inputValue }])
      setInputValue('')
      setShowWelcome(false)
      // Simulate bot response
      setTimeout(() => {
        //@ts-ignore
        setMessages(prev => [...prev, { type: 'bot', content: "I'm processing your query..." }])
      }, 1000)
    }
  }

  const startNewChat = () => {
    setMessages([])
    setShowWelcome(true)
    setShowInput(false)
    setIsSidebarOpen(false)
    setChatSessions(prev => [...prev, { id: Date.now(), title: "New Chat" }])
  }
//@ts-ignore
  const handleQuickPrompt = (prompt) => {
    if (prompt === 'Know Your Case Status') {
      setShowCaseForm(true);
    } else if (prompt === 'Present Live Streaming of Court Cases') {
      setShowCourtSelect(true);
    } else {
      setInputValue(prompt);
      setShowWelcome(false);
      handleSend();
    }
  };

  const handleCaseSubmit = () => {
    const prompt = `Give me the case summary of Diary No ${caseDetails.diaryNo} and Diary Year ${caseDetails.diaryYear}`
    setInputValue(prompt)
    setShowCaseForm(false)
    setShowWelcome(false)
    setShowInput(true)
    handleSend()
  }

  const handleCourtSubmit = () => {
    const prompt = `Give me current live stream of the ${selectedCourt}`
    setInputValue(prompt)
    setShowCourtSelect(false)
    setShowWelcome(false)
    setShowInput(true)
  }

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
              <Button onClick={startNewChat} className="w-full mb-4 bg-purple-600 hover:bg-purple-700 text-white px-8">
                <PlusCircle className="mr-2 h-4 w-4" /> New Chat
              </Button>
              <div className="space-y-2">
                {chatSessions.map((session) => (
                  <div key={session.id} className="text-sm p-2 rounded hover:bg-purple-100 dark:hover:bg-gray-700 cursor-pointer">
                    {session.title}
                  </div>
                ))}
              </div>
            </div>
          </SheetContent>
        </Sheet>
        
        <div className="flex items-center gap-2">
          <Gavel className="w-6 h-6 text-purple-600 dark:text-purple-400" />
          <span className="text-xl font-semibold text-purple-600 dark:text-purple-400">NyayDost</span>
        </div>
        
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon">
              <User className="w-6 h-6" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <LogOut className="mr-2 h-4 w-4" /> Logout
            </DropdownMenuItem>
            <DropdownMenuItem onSelect={() => setIsDarkMode(!isDarkMode)}>
              {isDarkMode ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
              {isDarkMode ? 'Light' : 'Dark'} Mode
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              
              <a href="https://w198wask7qd.typeform.com/to/mU16VTCT" target="_blank">Fill a Survey Form</a>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </header>

      {/* Welcome Screen / Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 px-8 md:px-16 lg:px-24">
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
            <Button onClick={() => setShowInput(true)} className="bg-purple-600 hover:bg-purple-700 text-white">Get Started</Button>
          </div>
        ) : (
          messages.map((message, index) => (
            
            <div
              key={index}
              //@ts-ignore
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  //@ts-ignore
                  message.type === 'user'
                    ? 'bg-purple-600 text-white dark:bg-purple-700 rounded-br-none'
                    : 'bg-white text-gray-800 dark:bg-gray-700 dark:text-white rounded-bl-none'
                }`}
              >
                {//@ts-ignore
                message.content}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Input Area */}
      {(showInput || !showWelcome) && (
        <div className="p-4 bg-white dark:bg-gray-800 border-t dark:border-gray-700">
          <div className="flex gap-2 max-w-4xl mx-auto px-8">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" size="icon" className="mr-2">
                  <Menu className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onSelect={() => handleQuickPrompt('Know Your Case Status')}>
                  Know Your Case Status
                </DropdownMenuItem>
                <DropdownMenuItem onSelect={() => handleQuickPrompt('Present Live Streaming of Court Cases')}>
                  Live Court Hearing
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
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
      )}

      {/* Case Status Form Dialog */}
      <Dialog open={showCaseForm} onOpenChange={setShowCaseForm}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Enter Case Details</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="diaryNo">Diary Number</Label>
              <Input
                id="diaryNo"
                placeholder="Enter Diary Number"
                value={caseDetails.diaryNo}
                onChange={(e) => setCaseDetails({ ...caseDetails, diaryNo: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="diaryYear">Diary Year</Label>
              <Input
                id="diaryYear"
                placeholder="Enter Diary Year"
                value={caseDetails.diaryYear}
                onChange={(e) => setCaseDetails({ ...caseDetails, diaryYear: e.target.value })}
              />
            </div>
            <Button onClick={handleCaseSubmit} className="w-full">
              Submit
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Court Selection Dialog */}
      <Dialog open={showCourtSelect} onOpenChange={setShowCourtSelect}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Select Court for Live Streaming</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <Select onValueChange={setSelectedCourt}>
              <SelectTrigger>
                <SelectValue placeholder="Select a court" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Supreme Court of India">Supreme Court of India</SelectItem>
                <SelectItem value="Gujarat High Court">Gujarat High Court</SelectItem>
                <SelectItem value="Karnataka High Court">Karnataka High Court</SelectItem>
                <SelectItem value="Delhi High Court">Delhi High Court</SelectItem>
                <SelectItem value="Bombay High Court">Bombay High Court</SelectItem>
                <SelectItem value="Patna High Court">Patna High Court</SelectItem>
                <SelectItem value="Gauhati High Court">Gauhati High Court</SelectItem>
                <SelectItem value="Calcutta High Court">Calcutta High Court</SelectItem>
                <SelectItem value="Madras High Court">Madras High Court</SelectItem>
                <SelectItem value="Allahabad High Court">Allahabad High Court</SelectItem>
                <SelectItem value="Andhra Pradesh High Court">Andhra Pradesh High Court</SelectItem>
                <SelectItem value="Chattisgarh High Court">Chattisgarh High Court</SelectItem>
                <SelectItem value="Himachal Pradesh High Court">Himachal Pradesh High Court</SelectItem>
                <SelectItem value="Jammu & Kashmir High Court">Jammu & Kashmir High Court</SelectItem>
                <SelectItem value="Jharkhand High Court">Jharkhand High Court</SelectItem>
                <SelectItem value="Kerala High Court">Kerala High Court</SelectItem>
                <SelectItem value="Madhya Pradesh High Court">Madhya Pradesh High Court</SelectItem>
                <SelectItem value="Meghalaya High Court">Meghalaya High Court</SelectItem>
                <SelectItem value="Orissa High Court">Orissa High Court</SelectItem>
                <SelectItem value="Punjab & Haryana High Court">Punjab & Haryana High Court</SelectItem>
                <SelectItem value="Rajasthan High Court">Rajasthan High Court</SelectItem>
                <SelectItem value="Sikkim High Court">Sikkim High Court</SelectItem>
                <SelectItem value="Telangana High Court">Telangana High Court</SelectItem>
                <SelectItem value="Tripura High Court">Tripura High Court</SelectItem>
                <SelectItem value="Uttarakhand High Court">Uttarakhand High Court</SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={handleCourtSubmit} className="w-full" disabled={!selectedCourt}>
              Submit
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Help Guide Dialog */}
      <Dialog>
        <DialogTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            className="fixed bottom-20 right-4 rounded-full shadow-lg"
          >
            <HelpCircle className="w-6 h-6" />
          </Button>
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>How to Use NyayDost</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <p>Welcome to NyayDost, your AI legal assistant!</p>
            <ul className="list-disc pl-4 space-y-2">
              <li>Click on any of the quick options or "Get Started" to begin</li>
              <li>Type your legal queries in the chat</li>
              <li>Use quick prompts from  the menu for common requests</li>
              <li>For case status, provide the Diary Number and Year</li>
              <li>For live court cases, select the specific court</li>
              <li>Access your chat history from the side menu</li>
              <li>Start a new chat session anytime</li>
              <li>Toggle between light and dark mode for comfort</li>
              <li>Provide feedback through the survey in the profile menu</li>
            </ul>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}