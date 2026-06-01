import { useState, type ChangeEvent } from "react";

interface Note {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

interface User {
  id: number;
  email: string;
  auth_provider_id: string;
}

const mockNotes: Note[] = [
  {
    id: 1,
    title: "React Hooks Guide",
    content:
      "# React Hooks\n\nHooks let you use state and other React features without writing a class.\n\n## useState\nManage component state...",
    created_at: "2024-01-15T10:30:00Z",
  },
  {
    id: 2,
    title: "TypeScript Basics",
    content:
      "# TypeScript Essentials\n\nTypeScript is a typed superset of JavaScript...",
    created_at: "2024-01-14T14:20:00Z",
  },
  {
    id: 3,
    title: "PostgreSQL with pgvector",
    content:
      "# Vector Search in PostgreSQL\n\nUsing pgvector extension for semantic search...",
    created_at: "2024-01-13T09:15:00Z",
  },
];

function App() {
  const [notes, setNotes] = useState(mockNotes);
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.currentTarget.value);
  };

  return (
    <>
      <h1>Recall IO</h1>
      <SearchInput
        inputAttr={{
          searchTerm: searchTerm,
          onSearch: handleSearch,
          id: "search",
          type: "text",
          placeholder: "Search...",
        }}
        isFocused
      />
      <List list={notes} />
    </>
  );
}

type SearchProps = {
  inputAttr: {
    placeholder: string;
    id: string;
    type?: string;
    searchTerm: string;
    onSearch: (event: ChangeEvent<HTMLInputElement>) => void;
  };
  isFocused: boolean;
};

function SearchInput({ inputAttr, isFocused }: SearchProps) {
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    inputAttr.onSearch(event);
  };

  return (
    <>
      <div className="search-container">
        <input
          placeholder={inputAttr.placeholder}
          id={inputAttr.id}
          type={inputAttr.type || "text"}
          value={inputAttr.searchTerm}
          onChange={handleChange}
          autoFocus={isFocused}
        />
      </div>
    </>
  );
}

type ListProps = {
  list: Note[];
};

function List({ list }: ListProps) {
  return (
    <>
      {list.map((item: Note) => (
        <Item key={item.id} item={item} />
      ))}
    </>
  );
}

type ItemProps = {
  item: Note;
};

function Item({ item }: ItemProps) {
  return (
    <>
      <span>{item.title}</span>
      <p>{item.content}</p>
      <span>{item.created_at}</span>
    </>
  );
}

export default App;
