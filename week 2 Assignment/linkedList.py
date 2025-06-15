class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        
    def add_node(self,data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
    
        current = self.head
        while current.next:
            current  = current.next
        current.next = new_node
        
    def print_list(self):
        if not self.head:
            print("The list is empty")
            return
    
        current = self.head
        while current:
            print(current.data, end = "->")
            current = current.next
        print("None")
    
    
    def delete_nth_node(self,n):
        try:
            if not self.head:
                raise Exception("Cannot delete from an empty list")
        
            if n<=0:
                raise IndexError("Index must be 1 or greater")
        
            if n==1:
                delete_data = self.head.data
                self.head = self.head.next
                print(f"Deleted node {n} with value '{deleted_data}'")
                return
        
            current = self.head
            for _ in range(n-2):
                if not current.next:
                    raise IndexError("Index out of range")
                current = current.next
            
            if not current.next:
                raise IndexError("Index out of range")
        
            deleted_data = current.next.data
            current.next = current.next.next
            print(f"Deleted node {n} with value '{deleted_data}'")
        
        except Exception as e:
            print(f"Error: {e}")
        
if __name__ == "__main__" :
    ll = LinkedList()
    
    ll.add_node(10)
    ll.add_node(20)
    ll.add_node(30)
    ll.add_node(40)
    ll.add_node(50)
    
    print("Initail List: ")
    ll.print_list()
    
    ll.delete_nth_node(3)
    ll.print_list()
    
    ll.delete_nth_node(1)
    ll.print_list()
    
    ll.delete_nth_node(10) #error
    ll.print_list()
    
    empty_list = LinkedList()
    empty_list.delete_nth_node(1)


